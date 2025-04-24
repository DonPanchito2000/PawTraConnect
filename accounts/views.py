from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import PetOwnerRegistrationForm, VetClinicRegistrationForm, ClubRegistrationForm, LoginForm
from django.http import HttpResponse

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
    if request.user.is_authenticated:
        # Redirect if already logged in (prevents CSRF from hitting back button)
        if request.user.role == 'owner':
            return redirect('pet-owner-dashboard')
        elif request.user.role == 'vet':
            return redirect('vet-clinic-dashboard')
        elif request.user.role == 'club':
            return redirect('club-dashboard')
        else:
            return HttpResponse('You are not allowed here')

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
                    return redirect('vet-clinic-dashboard')
                elif user.role == 'club':
                    return redirect('club-dashboard')
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