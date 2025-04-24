from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.choose_role, name='register'),
    path('register/pet-owner/', views.register_pet_owner, name='register_pet_owner'),
    path('register/vet-clinic/', views.register_vet_clinic, name='register_vet_clinic'),
    path('register/club/', views.register_club, name='register_club'),
]
