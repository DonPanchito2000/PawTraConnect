from django.contrib.auth.models import AbstractUser
from django.db import models

class Account(AbstractUser):
    email = models.EmailField(unique=True)
    USER_ROLES = (
        ('owner', 'Pet Owner'),
        ('vet', 'Vet Clinic'),
        ('club', 'Club'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"
    


class Barangay(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class PetOwnerProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    barangay = models.ForeignKey(Barangay, on_delete=models.SET_NULL, null=True)
    contact_number = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    social_email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.first_name} ({self.last_name})"

class VetClinicProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    clinic_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    social_email = models.EmailField(blank=True)
    is_city_vet = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.clinic_name} City Vet : ({self.is_city_vet})"
    

class ClubProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    club_name = models.CharField(max_length=100)
    admin_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    social_email = models.EmailField(blank=True)

    def __str__(self):
        return f"{self.club_name} ({self.admin_name})"

