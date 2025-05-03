from django.db import models
from accounts.models import Barangay, PetOwnerProfile

class Dog(models.Model):
    dog_id = models.CharField(max_length=150, unique=True, blank=True, null=True)

    pet_profile = models.ImageField(upload_to='pet_profile/', blank=True,null=True, default='pet_profile/default_pet_profile.png')
    name = models.CharField(max_length=100)
    breed  = models.CharField(max_length=200, blank=True)
    color = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    barangay = models.ForeignKey(Barangay, on_delete= models.SET_NULL, blank=True, null=True)
    owner = models.ForeignKey(PetOwnerProfile, on_delete=models.SET_NULL, blank=True, null=True)

    sex = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True) 

    

    def save(self, *args, **kwargs):
            if not self.dog_id:
                # Create a custom dog_id: combining dog's name, owner's name, and a count
                owner_name = self.owner.first_name[:3] if self.owner else "OWN"  # Default to "OWN" if owner is not defined
                dog_name = self.name[:3]  # Get the first 3 letters of the dog's name
                count = Dog.objects.count() + 1  # Get the count of dogs, ensuring unique IDs
                self.dog_id = f"{dog_name}-{owner_name}-{count:04d}"
            super().save(*args, **kwargs)