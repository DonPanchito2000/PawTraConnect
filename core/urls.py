from django.urls import path
from . import views

urlpatterns = [
    # -----------------------
    # PET_OWNER URLS
    # -----------------------
    path('pet-owner-dashboard/', views.pet_owner_dashboard,name='pet-owner-dashboard'),
    path('register-dog/',views.register_dog,name='register-dog'),
    path('dog-profile/<str:pk>', views.dog_profile,name='dog-profile'),
    # path('ccvo-announcement-page/', views.ccvo_announcement_page, name='ccvo-announcement-page'),
    path('club-page/', views.club_page, name='club-page'),
    path('join-club/<str:pk>', views.join_club, name='join-club'),
    path('cancel-request/<str:club_id>', views. cancel_request, name = 'cancel-request'),
    path('club-profile-page/<str:club_id>', views.club_profile_page, name ='club-profile-page'),
    path('club-forum-form/<str:club_id>',views.club_forum_form,name='club-forum-form'),
    path('get-club-forum-rooms/', views.getClubForumRooms, name='get-club-forum-rooms'),
    path('club-room-page/<int:pk>',views.club_room,name='club-room-page'),
    path('edit-pet-profile/<str:pet_id>/', views.edit_pet_profile , name ='edit-pet-profile'),
    # -----------------------
    # END PET_OWNER URLS
    # -----------------------
    

    # -----------------------
    # CLUB URLS
    # -----------------------
    path('club-announcement/', views.club_announcement,name='club-announcement'),
    path('club-announcement-form/', views.club_announcement_form, name="club-announcement-form"),
    path('member-page/', views.member_page, name='member-page'),
    path('accept-membership-request/<str:membership_id>', views.accept_membership_request, name='accept-membership-request'),
    path('reject-membership-request/<str:membership_id>', views.reject_membership_request, name='reject-membership-request'),
    path('kick-member-confirmation-page/<str:membership_id>', views.kick_member_confirmation_page, name='kick-member-confirmation-page'),
    path('kick-member/<str:membership_id>', views.kick_member, name='kick-member'),
    path('club-forum-page/', views.club_forum_page, name='club-forum-page'),
    path('club-form/', views.club_form, name='club-form'),
    path('club-announcement-room/<str:pk>/', views.club_announcement_room, name= "club-announcement-room"),
    # -----------------------
    # END CLUB URLS
    # -----------------------
    
    # -----------------------
    # VET URLS
    # -----------------------
    path('vet-clinic-dashboard/', views.vet_clinic_dashboard,name='vet-clinic-dashboard'),
    path('pending-approval-page/', views.pending_approval_page, name="pending-approval-page"),
    path('add-past-client/<str:owner_id>', views.add_past_client, name='add-past-client'),
    path('owner-pets-page/<str:owner_id>', views.owner_pets_page, name='owner-pets-page'),
    # -----------------------
    # END VET URLS
    # -----------------------

    # -----------------------
    # CCVO URLS
    # -----------------------
    # path('ccvo-dashboard/', views.ccvo_dashboard,name='ccvo-dashboard'),
    path('ccvo-announcement/', views.ccvo_announcement,name='ccvo-announcement'),
    path('approve-clinics-page/', views.approve_clinics_page, name="approve-clinics-page"),
    path('clinic-details/<str:clinic_id>/', views.view_clinic_details, name="clinic-details"),
    path('approve-clinic/<str:pk>/',views.approve_clinic, name='approve-clinic'),
    path('ccvo-announcement-form/',views.ccvo_announcement_form,name='ccvo-announcement-form'),
    path('announcement-room/<str:pk>/', views.announcement_room, name= "announcement-room"),
    path('services-page', views.services_page, name= 'services-page'),
    path('add-service-form-page/', views.add_service_form_page , name='add-service-form-page'),
    path('add-service-record-form-page/', views.add_service_record, name='add-service-record'),
    path('add-service-record-form/<str:selected_pet_id>/', views.service_form, name='add-service-record-form'),
    path('service-report-page/<str:service_id>/', views.service_report, name='service-report-page'),
    # -----------------------
    # CCVO VET URLS
    # -----------------------


    path('general-forum/',views.general_forum_view,name='general-forum'),
    path('general-forum-form/',views.general_forum_form,name='general-forum-form'),
    path('room/<int:pk>',views.room,name='room'),
    path('user-forum-profile/<str:user_id>/', views.user_forum_profile, name ="user-forum-profile"),


    path('get-rooms/', views.getRooms, name='get-rooms'),


    path('get-announcements/', views.getAnnouncements, name='get-announcements'),

    path('get-club-announcements/<str:club_id>/', views.getClubAnnouncements, name='get-club-announcements'),

    # -----------------------
    # START Vaccination Record Related URLS
    # -----------------------
    path('vaccination-details-page/<str:vaccination_id>/<str:is_history>', views.vaccination_details_page, name='vaccination-details-page'),
    path('vaccine-information-form-page-update/<str:old_vaccination_record_id>', views.vaccine_information_form_page_update, name='vaccine-information-form-page-update'),
    path('vaccine-information-form-page-new/<str:pet_id>', views.vaccine_information_form_page_new, name='vaccine-information-form-page-new'),
    path('vaccination-record-history-page/<str:pet_id>', views.vaccination_record_history_page, name='vaccination-record-history-page'),
    # -----------------------
    # END Vaccination Record Related URLS
    # -----------------------
]
