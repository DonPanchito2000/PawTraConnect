from django.urls import path
from . import views
from .views import PasswordsChangeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.choose_role, name='register'),
    # path('change-password/', auth_views.PasswordChangeView.as_view(template_name = 'accounts/change_password.html'), name='change-password'),
    path('change-password/', PasswordsChangeView.as_view(template_name = 'accounts/change_password.html'), name='change-password'),
    path('register/pet-owner/', views.register_pet_owner, name='register_pet_owner'),
    path('register/vet-clinic/', views.register_vet_clinic, name='register_vet_clinic'),
    path('register/club/', views.register_club, name='register_club'),
    path('account-page/', views.account_page, name= "account-page"),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
]
