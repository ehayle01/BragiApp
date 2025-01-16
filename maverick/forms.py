#BragiApp\maverick\forms.py
from django import forms
from .models import Maverick

class MaverickForm(forms.ModelForm):
    class Meta:
        model = Maverick
        fields = ['name', 'bio', 'profile_picture', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
