from django.db import models
from accounts.models import Barangay, PetOwnerProfile, Account, ClubProfile,VetClinicProfile
from django.core.exceptions import ValidationError


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

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-updated_at', '-created_at']



class ForumRoom(models.Model):
     host = models.ForeignKey(Account, on_delete = models.SET_NULL,null=True)
     title = models.CharField(max_length=200, blank=True)
     content = models.TextField()
     participants = models.ManyToManyField(Account, related_name='participants',blank=True)
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     image = models.ImageField(upload_to='forum_images/', blank=True, null=True)

     def __str__(self):
        return self.title
    
     class Meta:
        ordering = ['-updated', '-created']


class ForumComment(models.Model):
    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    room = models.ForeignKey(ForumRoom, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated','-created']
    

    def __str__(self):
        return self.body[0:50]


class ClubMembership(models.Model):
    member = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    club = models.ForeignKey(ClubProfile, on_delete =models.CASCADE )
    joined_at = models.DateTimeField(auto_now_add=True)


    STATUS_CHOICE = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
        ('removed', 'Removed'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICE,default='pending')
    approved_at = models.DateTimeField(null=True,blank=True)
    rejected_at = models.DateTimeField(null=True,blank=True)
    kicked_at = models.DateTimeField(null=True,blank=True)
    permanently_banned = models.BooleanField(default=False)

    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-joined_at']

    def clean(self):
        if self.member.role != 'owner' or not hasattr(self.member, 'petownerprofile'):
            raise ValidationError("Only pet owners can be members of a club.")

    def __str__(self):
        return f"{self.member.email} - {self.club.club_name} [{self.status}]"




# CLUB FORUM MODELS
class ClubForumRoom(models.Model):
     host = models.ForeignKey(Account, on_delete = models.SET_NULL,null=True)
     title = models.CharField(max_length=200, blank=True)
     content = models.TextField()
     joined = models.ManyToManyField(Account, related_name='joined',blank=True)
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     image = models.ImageField(upload_to='club_forum_images/', blank=True, null=True)

     def __str__(self):
        return self.title
    
     class Meta:
        ordering = ['-updated', '-created']


class ClubForumComment(models.Model):
    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    room = models.ForeignKey(ClubForumRoom, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated','-created']
    

    def __str__(self):
        return self.body[0:50]
# CLUB FORUM MODELS END


class VaccinationRecord(models.Model):
    pet = models.ForeignKey(Dog, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=100)
    vaccine_brand = models.CharField(max_length=100, blank=True, null=True)
    date_administered = models.DateField()
    next_due_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    veterinarian_name = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    vet_clinic = models.ForeignKey(VetClinicProfile, on_delete=models.SET_NULL, null=True, blank=True)

    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created']
    

    def __str__(self):
        return f"{self.pet} - {self.vaccine_name} [{self.vet_clinic}] [{self.date_administered}]  [{self.next_due_date}]  [{self.is_completed}]"





# CCVO Announcement
class CCVOAnnouncement(models.Model):
     host = models.ForeignKey(Account, on_delete = models.SET_NULL,null=True)
     title = models.CharField(max_length=200, blank=True)
     content = models.TextField()
     created = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     image = models.ImageField(upload_to='ccvo_announcement_images/', blank=True, null=True)

     def __str__(self):
        return self.title
    
     class Meta:
        ordering = ['-updated', '-created']























































































    




    
    