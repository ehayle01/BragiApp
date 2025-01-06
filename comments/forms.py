#BragiApp\comments\forms.py
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only the content field by default

    # Optional parent field (for replies)
    parent = forms.ModelChoiceField(
        queryset=Comment.objects.all(), 
        required=False, 
        widget=forms.HiddenInput()  # To keep it hidden unless needed
    )
