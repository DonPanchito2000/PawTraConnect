from django import forms
from .models import Dog, ForumRoom

class DogRegistrationForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['pet_profile', 'name', 'breed', 'color', 'age', 'barangay','sex']
        widgets = {
            'pet_profile': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'id_pet_profile'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dog name'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed (optional)'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color (optional)'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age in years'}),
            'barangay': forms.Select(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
        }


# General Forum
class ForumRoomForm(forms.ModelForm):
    class Meta:
        model = ForumRoom
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room title',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write something about the room...',
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
        model = ForumRoom
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room title',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write something about the room...',
                'required': True
            }),
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',
                'onchange': 'previewImage(event)',
                'hidden': True,  # hide native input
                'id': 'image'
            })
        }