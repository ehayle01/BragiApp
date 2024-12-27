from django import forms
from django.contrib.auth.models import User  # The built-in User model

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Include other fields as necessary (like password)
