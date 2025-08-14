from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from .forms import DogRegistrationForm, ForumRoomForm, ClubForumRoomForm, CCVOAnnouncementForm, ClubAnnouncementForm
from .models import Dog, ForumRoom, ForumComment, ClubMembership, ClubForumRoom, ClubForumComment, VaccinationRecord, CCVOAnnouncement, ClubAnnouncement
from accounts.models import PetOwnerProfile, VetClinicProfile, ClubProfile, Account
from django.http import HttpResponse
from django.contrib import messages
from django.utils.timesince import timesince
from django.utils import timezone
from datetime import timedelta

from django.http import JsonResponse
from django.core.serializers import serialize
import json

from django.template.loader import render_to_string

from django.urls import reverse

# Create your views here.

# -----------------------
# PET_OWNER VIEWS
# -----------------------
@login_required(login_url='login')
def pet_owner_dashboard(request):
    query = request.GET.get('q') if request.GET.get('q') else ''
    user = request.user
    if user.role == 'owner':
         try:
            owner = PetOwnerProfile.objects.get(user=user)
            all_registered_dogs = Dog.objects.filter(owner=owner)
            if query:
                filtered_dogs = all_registered_dogs.filter(
                    Q(name__icontains=query) | Q(breed__icontains=query)
                )
            else:
                filtered_dogs = all_registered_dogs

            today = timezone.now().date()
            three_days = today + timedelta(days=3)
        
            upcoming_vaccinations = VaccinationRecord.objects.filter(is_completed=False,next_due_date__range=(today, three_days),pet__in=all_registered_dogs)
            overdue_vaccinations = VaccinationRecord.objects.filter(is_completed=False,next_due_date__lt=today, pet__in=all_registered_dogs)
            context = {'registered_dogs':filtered_dogs,'all_dogs': all_registered_dogs,   'upcoming_vaccinations':upcoming_vaccinations,'overdue_vaccinations':overdue_vaccinations}
            
            return render(request,'owner/dashboard.html',context)
         except PetOwnerProfile.DoesNotExist:
            return HttpResponse('You are not allowed here!')
    else:
        return HttpResponse('You are not allowed here!')



@login_required(login_url='login')
def register_dog(request):
    form = DogRegistrationForm()

    if request.method == 'POST':
        form = DogRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
           dog = form.save(commit=False)
           dog.owner = request.user.petownerprofile  # assuming the user is logged in and has a profile
           dog.save()
           return redirect('pet-owner-dashboard')
        else:
            form = DogRegistrationForm()

    context = {'form':form}
    return render(request,'owner/register_dog.html',context)

@login_required(login_url='login')
def dog_profile(request,pk):
    user_is_vet = False
    is_history = False
    # pet = Dog.objects.get(id=pk)
    dog = Dog.objects.get(id=pk)
    today = timezone.now().date()
    three_days = today + timedelta(days=3)
 
    upcoming_vaccinations = VaccinationRecord.objects.filter(
        is_completed=False,
        next_due_date__range=(today, three_days),
        pet = dog
    )

    overdue_vaccinations = VaccinationRecord.objects.filter(
    is_completed=False,
    next_due_date__lt=today,
    pet = dog
    )


    user = request.user

    if user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            user_is_vet = True
            context = {'dog':dog,'upcoming_vaccinations':upcoming_vaccinations,'overdue_vaccinations':overdue_vaccinations,'user_is_vet':user_is_vet,'is_history':is_history}
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/dog_profile.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/dog_profile.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            # fallback in case vet profile is missing
            return HttpResponse('You are not allowed here!')
        
    
    elif user.role == 'owner':
        context = {'dog':dog,'upcoming_vaccinations':upcoming_vaccinations,'overdue_vaccinations':overdue_vaccinations,'user_is_vet':user_is_vet,'is_history':is_history}
        return render(request, 'owner/dog_profile.html', context)
    
    else:
        return HttpResponse('You are not allowed here!')




def club_page(request):

    banned_memberships  = ClubMembership.objects.filter(member = request.user, permanently_banned =True)
    banned_club_ids = banned_memberships.values_list('club_id', flat=True)

    user_clubs = ClubMembership.objects.filter(member=request.user,status='approved')

     # Get clubs the user has joined
    user_memberships = ClubMembership.objects.filter(member=request.user,status__in=['approved', 'pending'])
    joined_club_ids = user_memberships.values_list('club_id', flat=True)

    query = request.GET.get('q') if request.GET.get('q') else ''

    clubs = ClubProfile.objects.filter(
        Q(club_name__icontains=query)
        ).annotate(
            approved_members_count=Count(
                'clubmembership',
                filter=Q(clubmembership__status='approved')
            )
        )  

    context = {'user_clubs':user_clubs, 'clubs':clubs,'joined_club_ids': joined_club_ids, 'user_memberships':user_memberships,'banned_club_ids': banned_club_ids}
    return render(request, 'owner/club.html', context)


def join_club(request, pk):
    print("🛠️ join_club view called with pk =", pk)
    if request.method == 'POST':
        club = ClubProfile.objects.get(id=pk)
        membership, created = ClubMembership.objects.get_or_create(member=request.user,club=club)

        if not created:
                if membership.permanently_banned:   
                    messages.error(request, "You cannot join this club again.")
                    return redirect('club-page')   
                if membership.status == 'removed' or membership.status == 'rejected':
                    membership.status = 'pending'
                    membership.joined_at = timezone.now()  # optional: reset time
                    membership.save()
                else:
                    # Already has a non-removed membership
                    return redirect('club-page')
                    print('JOINED')
    return redirect('club-profile-page' , club_id = pk)

    

def club_profile_page(request, club_id):
    # This is to display club forum rooms
    query = request.GET.get('q') if request.GET.get('q') else ''
    club = ClubProfile.objects.get(id=club_id)
    print(f"Query: {query}")
    rooms = ClubForumRoom.objects.filter(
    Q(club=club) & (
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(host__username__icontains=query)
    )
).order_by('-created')
    print(rooms.query)
    room_comments = ClubForumComment.objects.select_related('room').filter(user=request.user).order_by('-created')[:10]

    membership_status =''
    

    # ANNOUNCEMENTS
    announcements = ClubAnnouncement.objects.filter(host=club.user).order_by('-created')

    try:
        user_membership = ClubMembership.objects.get(club = club, member = request.user)

        if user_membership.status == 'approved':
            membership_status = 'approved'
        elif user_membership.status == 'rejected':
            membership_status = 'rejected'
        elif user_membership.permanently_banned:
            membership_status = 'banned'
        elif user_membership.status == 'removed' and user_membership.permanently_banned == False:
            membership_status = 'removed'
        else:
            membership_status = 'pending'
    except ClubMembership.DoesNotExist:
        membership_status = 'none'
  
    context = {'club':club,'membership_status':membership_status,'rooms':rooms,'room_comments':room_comments,'announcements':announcements}
    return render(request, 'owner/club_profile.html', context)


def getClubAnnouncements(request, club_id):
    query = request.GET.get('q', '')

    try:
        club = ClubProfile.objects.get(id=club_id)
        announcements = ClubAnnouncement.objects.filter(host=club.user)

        data = []

        for announcement in announcements:
            data.append({
                "id": announcement.id,
                "title": announcement.title,
                "content_truncated": announcement.content[:300]+ "..." if len(announcement.content) > 100 else announcement.content,
                "created_timesince": timesince(announcement.created) + " ago",
                "host": {
                    "username": announcement.host.username,
                    "profile_picture_url": announcement.host.profile_picture.url if announcement.host.profile_picture else "",
                },
                "image_url": announcement.image.url if announcement.image else "",
            })

        return JsonResponse({"announcements": data})
    
    except ClubProfile.DoesNotExist:
        return JsonResponse({"announcements": []}, status=404)

def club_forum_form(request, club_id):
    user = request.user
    is_member = False
    club = ClubProfile.objects.get(id=club_id)

    approved_memberships = ClubMembership.objects.filter(club = club, status = 'approved')
    for approved_membership in approved_memberships:
        if approved_membership.member == user:
            is_member =True

    if not is_member:
        return redirect('club-profile-page', club_id = club_id)

    if request.method == 'POST':
            form = ClubForumRoomForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save(commit=False)
                room.host = user
                room.club = club
                room.save()
                url = reverse('club-profile-page', kwargs={'club_id': club_id})
                return redirect(f'{url}?tab=forum&subtab=posts')
    else:
        form = ClubForumRoomForm()



    context ={'form':form, 'club':club}

    return render(request, 'owner/club_forum_form.html',context)


def getClubForumRooms(request):
    query = request.GET.get('q', '')
    club_id = request.GET.get('club_id')

    rooms = ClubForumRoom.objects.filter(
        Q(club_id=club_id) & (
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(host__email__icontains=query)
        )
    ).order_by('-created')

    data = []

    for room in rooms:
        data.append({
            "id": room.id,
            "title": room.title,
            "content_truncated": room.content[:300]+ "..." if len(room.content) > 100 else room.content,
            "created_timesince": timesince(room.created) + " ago",
            "host": {
                "username": room.host.username,
                "profile_picture_url": room.host.profile_picture.url if room.host.profile_picture else "",
            },
            "image_url": room.image.url if room.image else "",
            "joined_count": room.joined.count(),
        })

    return JsonResponse({"rooms": data})



def club_room(request, pk):
    user = request.user
    print("DEBUG ROOM ID:", pk)
    room = get_object_or_404(ClubForumRoom, id=pk)
    room_comments = room.clubforumcomment_set.all().order_by('created')
    participants = room.joined.all()

    context ={'room':room, 'room_comments':room_comments,'paricipants':participants}

    if request.method == 'POST':
       comment = ClubForumComment.objects.create(
           user = request.user,
           room = room,
           body = request.POST.get('body')
       )
       room.joined.add(request.user)
       return JsonResponse({
                    'user_profile': comment.user.profile_picture.url,
                    'user': comment.user.username,
                    'comment': comment.body,
                    'created': comment.created.strftime('%Y-%m-%d %H:%M:%S'),
                })
    
    # automatic view new comments ajax
    if request.GET.get("ajax") == "1":
        html = ""
        for comment in room_comments:
            html += f'''
            <div class="comment-card">
                <img src="{comment.user.profile_picture.url}" alt="User Profile" />
                <div class="comment-body">
                    <div class="username">{comment.user.username} <span class="time">· {timesince(comment.created)} ago</span></div>
                    <div class="comment-text">{comment.body}</div>
                </div>
            </div>
            '''
        return HttpResponse(html)
    
    if user.role == 'owner':
        return render(request, 'owner/club_room_page.html', context)
    else:
        return render(request, 'club/club_room_page.html', context)
    

    # if user.role == 'owner':
    #     return render(request, 'owner/room_page.html', context)

    # elif user.role == 'vet':
    #     try:
    #         vet_profile = VetClinicProfile.objects.get(user=user)
    #         if vet_profile.is_city_vet:
    #             return render(request, 'ccvo/room_page.html',context)
    #         elif vet_profile.is_approved:
    #             return render(request, 'vet/room_page.html',context)
    #         else:
    #             return HttpResponse('You are not allowed here!')

    #     except VetClinicProfile.DoesNotExist:
    #         # fallback in case vet profile is missing
    #         return HttpResponse('You are not allowed here!')

    # elif user.role == 'club':
    #     return render(request, 'club/room_page.html',context)

    # else:
    #     # optional fallback if role is not recognized
    #      return HttpResponse('You are not allowed here!')
# -----------------------
# END PET_OWNER VIEWS
# -----------------------



# -----------------------
# VET_CLINIC VIEWS
# -----------------------
@login_required(login_url='login')
def vet_clinic_dashboard(request):
    

    query = request.GET.get('q')
    pet_owners = PetOwnerProfile.objects.filter(owner_id=query)
    

    user =request.user
    if user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user = request.user)
            regular_clients = vet_profile.regular_clients.all()
            context = {'pet_owners':pet_owners,'regular_clients':regular_clients}
            # vet_profile = VetClinicProfile.objects.get(user=user)
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/dashboard.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/dashboard.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            return HttpResponse('You are not allowed here!')
    else:
        return HttpResponse('You are not allowed here!')


@login_required(login_url='login')
def pending_approval_page(request):
    return render(request, 'vet/pending_approval.html')

def add_past_client(request, owner_id):
    if request.method == 'POST':
        owner = PetOwnerProfile.objects.get(id =owner_id)
        vet_clinic = VetClinicProfile.objects.get(user = request.user)
        vet_clinic.regular_clients.add(owner)
        return redirect('owner-pets-page', owner_id)
    return redirect('vet-clinic-dashboard')

def owner_pets_page(request, owner_id):
    pet_owner = PetOwnerProfile.objects.get(id = owner_id)
    pets = Dog.objects.filter(owner = pet_owner)
    context = {'pet_owner':pet_owner,'pets':pets}

    user =request.user
    if user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/pets.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/pets.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            return HttpResponse('You are not allowed here!')

# -----------------------
# END VET_CLINIC VIEWS
# -----------------------



# -----------------------
# CLUB VIEWS
# -----------------------


# @login_required(login_url='login')
# def club_announcement(request):
#     return render(request,'club/announcement.html')



def club_announcement_form(request):
    user = request.user

    if request.method == 'POST':
            form = ClubAnnouncementForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save(commit=False)
                room.host = user
                room.save()
                return redirect('club-announcement')
    else:
        form = ClubAnnouncementForm()



    context ={'form':form}



    if user.role == 'club':
       return render(request,'club/announcement_form.html', context)

    else:
        # optional fallback if role is not recognized
        return HttpResponse('You are not allowed here!')
    

@login_required(login_url='login')
def club_announcement_room(request, pk):
    user = request.user
    announcement = get_object_or_404(ClubAnnouncement, id=pk)
    club = ClubProfile.objects.get(user = announcement.host)
    context ={'announcement':announcement,'club':club}

    if user.role == 'owner':
        return render(request, 'owner/club_announcement_room.html', context)

    elif user.role == 'club':
        return render(request, 'club/announcement_room.html', context)

    else:
        # optional fallback if role is not recognized
         return HttpResponse('You are not allowed here!')


@login_required(login_url='login')
def member_page(request):
    club = ClubProfile.objects.get(user=request.user)
    memberships = ClubMembership.objects.filter(club=club)
    membership_requests = []
    approved_requests = []
    for membership in memberships:
        if membership.status == 'approved':
            approved_requests.append(membership)
        elif membership.status == 'pending':
            membership_requests.append(membership)

    context = {'membership_requests':membership_requests, 'approved_requests':approved_requests,'club':club}

    return render(request, 'club/member.html', context)


def accept_membership_request(request,membership_id):
    membership = ClubMembership.objects.get(id = membership_id)
    if request.method == 'POST':
        membership.status ='approved'
        membership.save()
        return redirect('member-page')

    return render(request,'club/member.html')


def reject_membership_request(request, membership_id):
    membership = ClubMembership.objects.get(id = membership_id)
    if request.method == 'POST':
            membership.status ='rejected'
            membership.save()
            return redirect('member-page')
    return render(request,'club/member.html')


def kick_member_confirmation_page(request,membership_id):
    membership = ClubMembership.objects.get(id = membership_id)

    context = {'membership':membership}
    return render(request,'club/kick_member_confirmation.html', context)

def kick_member(request, membership_id):
    ban_user = request.POST.get('ban_user')
    membership = ClubMembership.objects.get(id =membership_id)
    print(membership)
    if request.method == 'POST':
        membership.status = 'removed'
        membership.kicked_at = timezone.now()
        if ban_user == 'yes':
         membership.permanently_banned = True
        membership.save()
        print(membership)
    return redirect('member-page')
    


def club_forum_page(request):
    club = ClubProfile.objects.get(user = request.user)

    query = request.GET.get('q') if request.GET.get('q') else ''
    print(f"Query: {query}")
    rooms = ClubForumRoom.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(host__username__icontains=query)
    ).order_by('-created')

    room_comments = ClubForumComment.objects.select_related('room').filter(user=request.user).order_by('-created')[:10]

    context = {'club':club,'rooms':rooms,'room_comments':room_comments}
    return render(request, 'club/club_forum_page.html', context)


def club_form(request):
    user = request.user
    club = ClubProfile.objects.get(user = request.user)



    if request.method == 'POST':
            form = ClubForumRoomForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save(commit=False)
                room.host = user
                room.club = club
                room.save()
                # url = reverse('club-profile-page', kwargs={'club_id': club_id})
                return redirect('club-forum-page')
    else:
        form = ClubForumRoomForm()



    context ={'form':form, 'club':club}

    return render(request, 'owner/club_forum_form.html',context)


@login_required(login_url='login')
def club_announcement(request):
    user = request.user
   # ANNOUNCEMENTS
    

    if user.role == 'club':
        try:
            club = ClubProfile.objects.get(user = user)
            announcements = ClubAnnouncement.objects.filter(host=club.user).order_by('-created')
            context = {'announcements':announcements,'club':club}
            return render(request, 'club/announcement.html', context)
        except ClubProfile.DoesNotExist:
            return HttpResponse('You are not allowed here!')
    else:
        return HttpResponse('You are not allowed here!')
    
    
   


# -----------------------
# END CLUB VIEWS
# -----------------------



# -----------------------
# CCVO VIEWS
# -----------------------
@login_required(login_url='login')
def ccvo_announcement(request):
    user = request.user
    is_cv = False
    announcements = CCVOAnnouncement.objects.all()

    

    if user.role == 'vet':  # Check if the user is a vet
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            if vet_profile.is_city_vet:  
                is_cv = True
                context = {'announcements':announcements,'is_cv':is_cv}
                return render(request, 'ccvo/announcement.html', context)
            else:
                # If the vet is not a city vet, redirect to another page (e.g., 'another_page')
                return HttpResponse('You are not allowed here!')  # Change 'another_page' to your desired URL name
        except VetClinicProfile.DoesNotExist:
            # No vet profile found for this user
            return redirect('login')  # Same as above, redirect to another page
    
    elif user.role == 'owner':
        context = {'announcements':announcements,'is_cv':is_cv}
        return render(request, 'owner/ccvo_announcement_page.html', context)

    else:
        # If the user is not a vet (i.e., pet owner or other role), redirect to another page
        return redirect('login')  # Change 'another_page' to your desired URL name
    



def announcement_room(request, pk):
    user = request.user

    announcement = get_object_or_404(CCVOAnnouncement, id=pk)

    context ={'announcement':announcement}

    if user.role == 'owner':
        return render(request, 'owner/announcement_room.html', context)

    elif user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/announcement_room.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            # fallback in case vet profile is missing
            return HttpResponse('You are not allowed here!')
        
    elif user.role == "club":
        return render(request, 'club/announcement_room.html', context)

    else:
        # optional fallback if role is not recognized
         return HttpResponse('You are not allowed here!')

    

def getAnnouncements(request):
    query = request.GET.get('q', '')

    announcements = CCVOAnnouncement.objects.all()

    data = []

    for announcement in announcements:
        data.append({
            "id": announcement.id,
            "title": announcement.title,
            "content_truncated": announcement.content[:300]+ "..." if len(announcement.content) > 100 else announcement.content,
            "created_timesince": timesince(announcement.created) + " ago",
            "host": {
                "username": announcement.host.username,
                "profile_picture_url": announcement.host.profile_picture.url if announcement.host.profile_picture else "",
            },
            "image_url": announcement.image.url if announcement.image else "",
        })

    return JsonResponse({"announcements": data})


def ccvo_announcement_form(request):
    user = request.user

    if request.method == 'POST':
            form = CCVOAnnouncementForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save(commit=False)
                room.host = user
                room.save()
                return redirect('ccvo-announcement')
    else:
        form = CCVOAnnouncementForm()



    context ={'form':form}



    if user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/announcement_form.html',context)
      
            else:
                 return HttpResponse('You are not allowed here!')
        except VetClinicProfile.DoesNotExist:
            # fallback in case vet profile is missing
           return HttpResponse('You are not allowed here!')

    else:
        # optional fallback if role is not recognized
        return HttpResponse('You are not allowed here!')




@login_required(login_url='login')
def approve_clinics_page(request):
    # Get all unapproved clinics
    pending_clinics = VetClinicProfile.objects.filter(is_approved=False)

    # Exclude the currently logged-in user's clinic (if they have one)
    approved_clinics = VetClinicProfile.objects.filter(is_approved=True).exclude(user=request.user)

    context = {'pending_clinics': pending_clinics,'approved_clinics': approved_clinics,}
    return render(request, 'ccvo/approve_clinics.html', context)


def approve_clinic(request, pk):
    clinic = get_object_or_404(VetClinicProfile, id=pk)

    if request.method == 'POST':
        clinic.is_approved=True
        clinic.save()
        return redirect('approve-clinics-page')

    return render(request,'ccvo/approve_clinics.html')


# @login_required(login_url='login')
# def ccvo_dashboard(request):
#     user = request.user
#     vet_profile = VetClinicProfile.objects.get(user=user)
#     if not vet_profile.is_city_vet:
#          return HttpResponse('You are not allowed here!')
#     return render(request,'ccvo/dashboard.html')
# -----------------------
# END CCVO VIEWS
# -----------------------




# -----------------------
# GENERAL FORUM VIEWS
# -----------------------

@login_required
def general_forum_view(request):

    query = request.GET.get('q') if request.GET.get('q') else ''
    # print(f"Query: {query}")
    rooms = ForumRoom.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(host__username__icontains=query)
    ).order_by('-created')

    # Recent comments/messages
    room_comments = ForumComment.objects.select_related('room').filter(user=request.user).order_by('-created')[:10]


    context = {
        'rooms': rooms,
        'room_comments': room_comments,
    }

    user = request.user

    if user.role == 'owner':
        return render(request, 'owner/forum.html',context)

    elif user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/forum.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/forum.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            # fallback in case vet profile is missing
            return HttpResponse('You are not allowed here!')

    elif user.role == 'club':
        return render(request, 'club/forum.html',context)

    else:
        # optional fallback if role is not recognized
         return HttpResponse('You are not allowed here!')
    


def general_forum_form(request):
    user = request.user

    if request.method == 'POST':
            form = ForumRoomForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save(commit=False)
                room.host = user
                room.save()
                return redirect('general-forum')
    else:
        form = ForumRoomForm()



    context ={'form':form}

    if user.role == 'owner':
        return render(request, 'owner/forum_form.html',context)

    elif user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/forum_form.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/forum_form.html',context)
            else:
                 return HttpResponse('You are not allowed here!')
        except VetClinicProfile.DoesNotExist:
            # fallback in case vet profile is missing
           return HttpResponse('You are not allowed here!')

    elif user.role == 'club':
        return render(request, 'club/forum_form.html',context)

    else:
        # optional fallback if role is not recognized
        return HttpResponse('You are not allowed here!')





def room(request, pk):
    user = request.user

    room = get_object_or_404(ForumRoom, id=pk)
    room_comments = room.forumcomment_set.all().order_by('created')
    participants = room.participants.all()

    context ={'room':room, 'room_comments':room_comments,'paricipants':participants}

    if request.method == 'POST':
       comment = ForumComment.objects.create(
           user = request.user,
           room = room,
           body = request.POST.get('body')
       )
       room.participants.add(request.user)
       return JsonResponse({
                    'user_profile': comment.user.profile_picture.url,
                    'user': comment.user.username,
                    'comment': comment.body,
                    'created': comment.created.strftime('%Y-%m-%d %H:%M:%S'),
                })
    
    # automatic view new comments ajax
    if request.GET.get("ajax") == "1":
        html = ""
        for comment in room_comments:
            html += f'''
            <div class="comment-card">
                <img src="{comment.user.profile_picture.url}" alt="User Profile" />
                <div class="comment-body">
                    <div class="username">{comment.user.username} <span class="time">· {timesince(comment.created)} ago</span></div>
                    <div class="comment-text">{comment.body}</div>
                </div>
            </div>
            '''
        return HttpResponse(html)

    if user.role == 'owner':
        return render(request, 'owner/room_page.html', context)

    elif user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/room_page.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/room_page.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            # fallback in case vet profile is missing
            return HttpResponse('You are not allowed here!')

    elif user.role == 'club':
        return render(request, 'club/room_page.html',context)

    else:
        # optional fallback if role is not recognized
         return HttpResponse('You are not allowed here!')



def getRooms(request):
    query = request.GET.get('q', '')

    rooms = ForumRoom.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(host__email__icontains=query)
    ).order_by('-created')

    data = []

    for room in rooms:
        data.append({
            "id": room.id,
            "title": room.title,
           "content_truncated": (room.content[:300] + "...") if len(room.content) > 300 else room.content,
            "created_timesince": timesince(room.created) + " ago",
            "host": {
                "id": room.host.id if room.host else None,
                "username": room.host.username if room.host else "Unknown",
                "profile_picture_url": room.host.profile_picture.url if room.host.profile_picture else "",
            },
            "image_url": room.image.url if room.image else "",
            "participants_count": room.participants.count(),
        })

    return JsonResponse({"rooms": data})


def user_forum_profile(request, user_id):
    user = Account.objects.get(id = user_id)
    context = {'user':user}
    return render(request, 'owner/user_forum_profile.html', context)

# -----------------------
# END GENERAL FORUM VIEWS
# -----------------------


# -----------------------
# START VACCINATION RECORD RELATED VIEWS
# -----------------------
def vaccination_details_page(request, vaccination_id, is_history):
    user = request.user
    user_is_vet = False
    vaccination_record = VaccinationRecord.objects.get(id = vaccination_id)
    is_history = is_history.lower() == 'true'

    if user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            user_is_vet =True

            context ={'vaccination_record':vaccination_record,'user_is_vet':user_is_vet,'is_history':is_history}

            if vet_profile.is_city_vet:
                return render(request, 'ccvo/vaccination_details.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/vaccination_details.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            return HttpResponse('You are not allowed here!')
        

    elif user.role == 'owner':
        context = {
            'vaccination_record': vaccination_record,
            'user_is_vet': user_is_vet,
            'is_history':is_history
        }
        return render(request, 'owner/vaccination_details.html', context)

    else:
         return HttpResponse('You are not allowed here!')
    

@login_required(login_url='login')
def vaccine_information_form_page_update(request, old_vaccination_record_id):
     user = request.user
     old_vaccination_record = VaccinationRecord.objects.get(id = old_vaccination_record_id)
     vet_clinic = VetClinicProfile.objects.get(user=user)
     if request.method == "POST":
        pet_id = request.POST.get('pet')
        try:
            next_due_date_raw = request.POST.get('next_due_date')
            next_due_date = next_due_date_raw if next_due_date_raw else None
            pet = Dog.objects.get(id = pet_id)
            VaccinationRecord.objects.create(
                pet = pet,
                vaccine_name = request.POST.get('vaccine_name'),
                vaccine_brand = request.POST.get('vaccine_brand'),
                date_administered = request.POST.get('date_administered'),
                next_due_date = next_due_date,
                veterinarian_name = request.POST.get('veterinarian_name'),
                license_number = request.POST.get('license_number'),
                vet_clinic = vet_clinic,
                notes = request.POST.get('notes')
            )
            old_vaccination_record.is_completed = True
            old_vaccination_record.save()
            return redirect('dog-profile', pk = pet_id)
        except Dog.DoesNotExist:  
             return HttpResponse("Pet not found", status=404)
         
     if user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            context = {'old_vaccination_record':old_vaccination_record,'vet_profile':vet_profile}
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/vaccine_information_form.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/vaccine_information_form.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            return HttpResponse('You are not allowed here!')
        



def vaccine_information_form_page_new(request, pet_id):
     user = request.user
     vet_clinic = VetClinicProfile.objects.get(user=user)
     pet = Dog.objects.get(id = pet_id)
     if request.method == "POST":
        try:
            next_due_date_raw = request.POST.get('next_due_date')
            next_due_date = next_due_date_raw if next_due_date_raw else None
            VaccinationRecord.objects.create(
                pet = pet,
                vaccine_name = request.POST.get('vaccine_name'),
                vaccine_brand = request.POST.get('vaccine_brand'),
                date_administered = request.POST.get('date_administered'),
                next_due_date = next_due_date,
                veterinarian_name = request.POST.get('veterinarian_name'),
                license_number = request.POST.get('license_number'),
                vet_clinic = vet_clinic,
                notes = request.POST.get('notes')
            )
            return redirect('dog-profile', pk = pet_id)
        except Dog.DoesNotExist:  
             return HttpResponse("Pet not found", status=404)
         
     if user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)
            context = {'vet_profile':vet_profile,'pet':pet}
            if vet_profile.is_city_vet:
                return render(request, 'ccvo/vaccine_information_form.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/vaccine_information_form.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            return HttpResponse('You are not allowed here!')
        



def vaccination_record_history_page(request, pet_id):
    user = request.user
    pet = Dog.objects.get(id = pet_id)
    is_history = True
    pet_vaccination_records = VaccinationRecord.objects.filter(pet=pet)

    context = {'pet':pet,'pet_vaccination_records':pet_vaccination_records,'is_history':is_history}
    if user.role == 'vet':
        try:
            vet_profile = VetClinicProfile.objects.get(user=user)

            if vet_profile.is_city_vet:
                return render(request, 'ccvo/vaccination_record_history.html',context)
            elif vet_profile.is_approved:
                return render(request, 'vet/vaccination_record_history.html',context)
            else:
                return HttpResponse('You are not allowed here!')

        except VetClinicProfile.DoesNotExist:
            return HttpResponse('You are not allowed here!')
        

    elif user.role == 'owner':

        return render(request, 'owner/vaccination_record_history.html', context)

    else:
         return HttpResponse('You are not allowed here!')
# -----------------------
# END VACCINATION RECORD RELATED VIEWS
# -----------------------