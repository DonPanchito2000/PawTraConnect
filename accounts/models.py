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
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='profile_pics/defaultprofile.png')

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

    owner_id = models.CharField(max_length=50, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.owner_id:
            prefix = f"{self.first_name[:3].upper()}-{self.last_name[:3].upper()}"
            count = PetOwnerProfile.objects.count() + 1
            self.owner_id = f"{prefix}-{count:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} ({self.last_name})"

class VetClinicProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    clinic_name = models.CharField(max_length=100)
    business_permit_number = models.CharField(max_length=100)
    issuing_office = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    is_city_vet = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    regular_clients = models.ManyToManyField('PetOwnerProfile', related_name='linked_vets', blank=True)

    def __str__(self):
        return f"{self.clinic_name} City Vet : ({self.is_city_vet})"
    

class ClubProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    club_name = models.CharField(max_length=100)
    admin_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    admin_email = models.EmailField(blank=True)
    
     # Optional fields
    has_professional_services = models.BooleanField(default=False)

    # CPC and PTR file uploads (optional, but useful for verification)
    cpc_document = models.FileField(upload_to='cpc_docs/', null=True, blank=True)
    ptr_document = models.FileField(upload_to='ptr_docs/', null=True, blank=True)

    # Dates of issuance (optional)
    cpc_issued_date = models.DateField(null=True, blank=True)
    ptr_issued_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.club_name} ({self.admin_name})"

