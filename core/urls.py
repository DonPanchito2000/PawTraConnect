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
    path('pending-approval-page/', views.pending_approval_page, name="pending-approval-page"),
    # -----------------------
    # END VET URLS
    # -----------------------

    # -----------------------
    # CCVO URLS
    # -----------------------
    path('ccvo-announcement/', views.ccvo_announcement,name='ccvo-announcement'),
    path('approve-clinics-page/', views.approve_clinics_page, name="approve-clinics-page"),
    path('approve-clinic/<str:pk>',views.approve_clinic, name='approve-clinic'),
    # -----------------------
    # CCVO VET URLS
    # -----------------------

]
