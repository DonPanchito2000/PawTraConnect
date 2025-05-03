from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account, PetOwnerProfile, VetClinicProfile, ClubProfile, Barangay

# Pet Owner
class PetOwnerRegistrationForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    contact_number = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea)
    barangay = forms.ModelChoiceField(queryset=Barangay.objects.all())
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'owner'
        user.set_password(self.cleaned_data['password1'])
        user.profile_picture = self.cleaned_data['profile_picture']
        if commit:
            user.save()
            PetOwnerProfile.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                contact_number=self.cleaned_data['contact_number'],
                barangay=self.cleaned_data['barangay'],
                bio=self.cleaned_data['bio'],
            )
        return user


class VetClinicRegistrationForm(UserCreationForm):
    clinic_name = forms.CharField()
    business_permit_number = forms.CharField()
    issuing_office = forms.CharField()
    contact_number = forms.CharField()
    location = forms.CharField()
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'vet'
        if commit:
            user.save()
            VetClinicProfile.objects.create(
                user=user,
                clinic_name=self.cleaned_data['clinic_name'],
                business_permit_number=self.cleaned_data['business_permit_number'],
                issuing_office=self.cleaned_data['issuing_office'],
                contact_number=self.cleaned_data['contact_number'],
                location=self.cleaned_data['location'],
                is_city_vet=False, # always default to False
                is_approved=False 
            )
        return user



class ClubRegistrationForm(UserCreationForm):
    club_name = forms.CharField()
    admin_name = forms.CharField()
    contact_number = forms.CharField()
    description = forms.CharField(widget=forms.Textarea)
    profile_picture = forms.ImageField(required=False)
    admin_email = forms.EmailField(required=True)
    class Meta:
        model = Account
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'club'
        if commit:
            user.save()
            ClubProfile.objects.create(
                user=user,
                club_name=self.cleaned_data['club_name'],
                admin_name=self.cleaned_data['admin_name'],
                contact_number=self.cleaned_data['contact_number'],
                description=self.cleaned_data['description'],
                admin_email=self.cleaned_data['admin_email']
            )
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
