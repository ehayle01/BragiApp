# backend/groups/forms.py
from django import forms
from .models import Group
from django.contrib.auth.models import User

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']

    # Optional: Add a custom method to add members in the form if needed
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

# backend/groups/forms.py
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'members']

    def clean_members(self):
        members = self.cleaned_data.get('members')
        if not members:
            raise forms.ValidationError("At least one member must be selected.")
        return members
