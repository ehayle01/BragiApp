# backend/groups/forms.py
from django import forms
from .models import Group
from django.contrib.auth.models import User
from followers.models import Follow

class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'cover_image', 'location']  # Correct fields

    # Override the __init__ method to filter members based on the users the current user is following
    def __init__(self, *args, **kwargs):
        # Get the current user from kwargs (sent from the view)
        self.user = kwargs.pop('user', None)  # Pop the user out of kwargs
        super().__init__(*args, **kwargs)

        if self.user:
            # Get the users the current user is following
            following = Follow.objects.filter(follower=self.user).select_related('followed')

            # Get the list of users that the current user is following
            followed_users = [follow.followed for follow in following]

            # Filter the members field to only show followed users
            self.fields['members'].queryset = User.objects.filter(id__in=[followed_user.id for followed_user in followed_users])

    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'cover_image', 'location', 'members']

    def clean_members(self):
        members = self.cleaned_data.get('members')
        if not members:
            raise forms.ValidationError("At least one member must be selected.")
        return members

