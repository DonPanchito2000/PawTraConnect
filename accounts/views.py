from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import PetOwnerRegistrationForm, VetClinicRegistrationForm, ClubRegistrationForm, LoginForm, EditPetOwnerProfileForm, EditVetClinicProfileForm, EditClubProfileForm, EditAccountForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def register_pet_owner(request):
    form = PetOwnerRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    else:
         print("Form errors:", form.errors)
    return render(request, 'accounts/register_pet_owner.html', {'form': form})


def register_vet_clinic(request):
    form = VetClinicRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'accounts/register_vet_clinic.html', {'form': form})


def register_club(request):
    form = ClubRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'accounts/register_club.html', {'form': form})



def choose_role(request):
    return render(request, 'accounts/choose_role.html')




def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')

                # Redirect based on user role
                if user.role == 'owner':
                    return redirect('pet-owner-dashboard')
                
                elif user.role == 'vet':
                    if hasattr(user, 'vetclinicprofile'):
                        vet_profile = user.vetclinicprofile

                        if vet_profile.is_city_vet:
                            return redirect('ccvo-announcement')
                        elif not vet_profile.is_approved:
                            return redirect('pending-approval-page')  # this should match your URL name
                        else:
                            return redirect('vet-clinic-dashboard')
                    else:
                        messages.error(request, 'Vet clinic profile not found.')
                        return redirect('login')
                    
                elif user.role == 'club':
                    return redirect('club-announcement')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    logout(request)
    _ = list(messages.get_messages(request))  # Clear any previous messages
    messages.success(request, 'You have been logged out.')
    return redirect('login')



# START ACCOUNT SETTING

def account_page(request):
    user = request.user
    context = {'user':user}
    return render(request, 'accounts/account.html', context)





@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        if user.role == 'owner':
            form = EditPetOwnerProfileForm(request.POST, instance=user.petownerprofile)
            account_form = EditAccountForm(request.POST, request.FILES, instance=user)
        elif user.role == 'club':
            form = EditClubProfileForm(request.POST, instance=user.clubprofile)
            account_form = EditAccountForm(request.POST, request.FILES, instance=user)
        elif user.role == 'vet':
            form = EditVetClinicProfileForm(request.POST, instance=user.vetclinicprofile)
            account_form = EditAccountForm(request.POST, request.FILES, instance=user)
        else:
            return redirect('login')

        if form.is_valid() and account_form.is_valid():
            form.save()
            account_form.save()
            return redirect('account-page')  # Or wherever you want to redirect after saving
    else:
        if user.role == 'owner':
            form = EditPetOwnerProfileForm(instance=user.petownerprofile)
            account_form = EditAccountForm(instance=user)
        elif user.role == 'club':
            form = EditClubProfileForm(instance=user.clubprofile)
            account_form = EditAccountForm(instance=user)
        elif user.role == 'vet':
            form = EditVetClinicProfileForm(instance=user.vetclinicprofile)
            account_form = EditAccountForm(instance=user)
        else:
            return redirect('login')

    context = {
        'form': form,
        'account_form': account_form,
        'user': user
    }
    return render(request, 'accounts/edit_profile.html', context)


# END ACCOUNT SETTING