from django.db import models
from accounts.models import Barangay, PetOwnerProfile

class Dog(models.Model):
    pet_profile = models.ImageField(upload_to='pet_profile/', blank=True,null=True, default='pet_profile/default_pet_profile.png')
    name = models.CharField(max_length=100)
    breed  = models.CharField(max_length=200, blank=True)
    color = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    barangay = models.ForeignKey(Barangay, on_delete= models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(PetOwnerProfile, on_delete=models.SET_NULL, blank=True, null=True)