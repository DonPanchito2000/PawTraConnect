from django.urls import path
from . import views

urlpatterns = [
    # -----------------------
    # PET_OWNER URLS
    # -----------------------
    path('pet-owner-dashboard/', views.pet_owner_dashboard,name='pet-owner-dashboard'),
    path('register-dog/',views.register_dog,name='register-dog'),
    path('dog-profile/<str:pk>', views.dog_profile,name='dog-profile'),
    path('ccvo-announcement-page/', views.ccvo_announcement_page, name='ccvo-announcement-page'),
    # -----------------------
    # END PET_OWNER URLS
    # -----------------------
    

    # -----------------------
    # PCLUB URLS
    # -----------------------
    path('club-announcement/', views.club_announcement,name='club-announcement'),
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
    path('ccvo-dashboard/', views.ccvo_dashboard,name='ccvo-dashboard'),
    path('ccvo-announcement/', views.ccvo_announcement,name='ccvo-announcement'),
    path('approve-clinics-page/', views.approve_clinics_page, name="approve-clinics-page"),
    path('approve-clinic/<str:pk>',views.approve_clinic, name='approve-clinic'),
    # -----------------------
    # CCVO VET URLS
    # -----------------------


    path('general-forum/',views.general_forum_view,name='general-forum'),
    path('general-forum-form/',views.general_forum_form,name='general-forum-form'),
]
