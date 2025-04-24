from django.urls import path
from . import views

urlpatterns = [
    # -----------------------
    # PET_OWNER URLS
    # -----------------------
    path('pet-owner-dashboard/', views.pet_owner_dashboard,name='pet-owner-dashboard'),
    path('register-dog/',views.register_dog,name='register-dog'),
    path('dog-profile/<str:pk>', views.dog_profile,name='dog-profile'),
    # -----------------------
    # END PET_OWNER URLS
    # -----------------------
    

    # -----------------------
    # PCLUB URLS
    # -----------------------
    path('club-dashboard/', views.club_dashboard,name='club-dashboard'),
    # -----------------------
    # END CLUB URLS
    # -----------------------
    
    # -----------------------
    # VET URLS
    # -----------------------
    path('vet-clinic-dashboard/', views.vet_clinic_dashboard,name='vet-clinic-dashboard'),
    # -----------------------
    # END VET URLS
    # -----------------------
]
