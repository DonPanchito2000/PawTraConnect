from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import DogRegistrationForm
from .models import Dog
from accounts.models import PetOwnerProfile, VetClinicProfile

# Create your views here.

# -----------------------
# PET_OWNER VIEWS
# -----------------------
def pet_owner_dashboard(request):
    owner =  get_object_or_404(PetOwnerProfile, user=request.user)
    registered_dogs= Dog.objects.filter(owner = owner)
    context = {'registered_dogs':registered_dogs}
    return render(request,'owner/dashboard.html',context)

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


def dog_profile(request,pk):
    dog = Dog.objects.get(id=pk)
    context = {'dog':dog}
    return render(request,'owner/dog_profile.html',context)

# -----------------------
# END PET_OWNER VIEWS
# -----------------------



# -----------------------
# VET_CLINIC VIEWS
# -----------------------
def vet_clinic_dashboard(request):
    return render(request,'vet/dashboard.html')


def pending_approval_page(request):
    return render(request, 'vet/pending_approval.html')
# -----------------------
# END VET_CLINIC VIEWS
# -----------------------



# -----------------------
# CLUB VIEWS
# -----------------------
def club_dashboard(request):
    return render(request,'club/dashboard.html')
# -----------------------
# END CLUB VIEWS
# -----------------------



# -----------------------
# CCVO VIEWS
# -----------------------
def ccvo_announcement(reuqest):
    return render(reuqest,'ccvo/announcement.html')


@login_required
def approve_clinics_page(request):
    # Get all unapproved clinics
    pending_clinics = VetClinicProfile.objects.filter(is_approved=False)

    # Exclude the currently logged-in user's clinic (if they have one)
    approved_clinics = VetClinicProfile.objects.filter(is_approved=True).exclude(user=request.user)

    context = {
        'pending_clinics': pending_clinics,
        'approved_clinics': approved_clinics,
    }
    return render(request, 'ccvo/approve_clinics.html', context)


# -----------------------
# END CCVO VIEWS
# -----------------------