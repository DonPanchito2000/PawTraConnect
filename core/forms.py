from django import forms
from .models import Dog, ForumRoom, ClubForumRoom, VaccinationRecord, CCVOAnnouncement, ClubAnnouncement, Service, ServiceRecord, Barangay

class DogRegistrationForm(forms.ModelForm):
    barangay = forms.ModelChoiceField(
        queryset=Barangay.objects.all().order_by('name'),
        widget=forms.Select(attrs={
            'class': 'form-control custom-select-style',
            'id': 'id_barangay'
        }),
        empty_label="Select Barangay"
    )

    class Meta:
        model = Dog
        fields = ['pet_profile', 'name', 'breed', 'color', 'age', 'barangay', 'sex']
        widgets = {
            'pet_profile': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'id_pet_profile'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dog name'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed (optional)'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color (optional)'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'sex': forms.Select(attrs={'class': 'form-control custom-select-style'}),
        }


# General Forum
class ForumRoomForm(forms.ModelForm):
    class Meta:
        model = ForumRoom
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room title...',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Room description...',
                'required': True
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'onchange': 'previewImage(event)',
                'hidden': True,  # hide native input
                'id': 'image'
            })
        }


    
# Club form
class ClubForumRoomForm(forms.ModelForm):
    class Meta:
        model = ClubForumRoom
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Room title...',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Room description...',
                'required': True
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'onchange': 'previewImage(event)',
                'hidden': True,  # hide native input
                'id': 'image'
            })
        }



# CCVO Annoucement Form 
class CCVOAnnouncementForm(forms.ModelForm):
    class Meta:
        model = CCVOAnnouncement
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Announcement title...',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Announcement description...',
                'required': True
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'onchange': 'previewImage(event)',
                'hidden': True,  # hide native input
                'id': 'image'
            })
        }


# CLUB Annoucement Form 
class ClubAnnouncementForm(forms.ModelForm):
    class Meta:
        model = ClubAnnouncement
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Announcement title...',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Announcement description...',
                'required': True
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'onchange': 'previewImage(event)',
                'hidden': True,  
                'id': 'image'
            })
        }


# Edit Pet Profile Form

class EditPetProfileForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['pet_profile', 'name', 'breed', 'color', 'age','sex','barangay']
        widgets = {
            'pet_profile': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'profilePictureInput'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'breed':forms.TextInput(attrs={'class': 'form-control', 'rows': 4}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'rows': 4}),
            'sex': forms.Select(attrs={'class': 'form-control custom-select-style'}),
            'barangay': forms.Select(attrs={'class': 'form-control custom-select-style'}),
            
        }


# Service Form
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Service Description (optional)'}),

        }



# class ServiceRecordForm(forms.ModelForm):
#     pet = forms.ModelChoiceField(
#         queryset=Dog.objects.all(),
#         to_field_name="id",  # search by Pet ID
#         widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Pet ID"})
#     )
    
#     service = forms.ModelChoiceField(
#         queryset=Service.objects.all(),
#         widget=forms.Select(attrs={"class": "form-control select2"})  # searchable dropdown
#     )

#     class Meta:
#         model = ServiceRecord
#         fields = ["pet", "service"] 