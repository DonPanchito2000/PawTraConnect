from django.contrib import admin
from .models import Account,PetOwnerProfile,VetClinicProfile, ClubProfile,Barangay
# Register your models here.

admin.site.register(Account)
admin.site.register(VetClinicProfile)
admin.site.register(ClubProfile)
admin.site.register(Barangay)
admin.site.register(PetOwnerProfile)