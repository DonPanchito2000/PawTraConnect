from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import DogRegistrationForm
from .models import Dog
from accounts.models import PetOwnerProfile

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