from django import forms
from .models import Dog

class DogRegistrationForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['pet_profile', 'name', 'breed', 'color', 'age', 'barangay']
        widgets = {
            'pet_profile': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'id': 'id_pet_profile'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dog name'}),
            'breed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breed (optional)'}),
            'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Color (optional)'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age in years'}),
            'barangay': forms.Select(attrs={'class': 'form-control'}),
        }