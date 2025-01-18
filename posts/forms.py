#BragiApp\posts\forms.py
from django import forms
from .models import Post
from maverick.models import Maverick  # Import Maverick model to use in the form
from filters.models import Category, Tag


class PostForm(forms.ModelForm):
    """Form for creating or editing a post."""

    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="Select a Category")
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags', 'maverick']  

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control rounded', 'placeholder': 'Write your content here...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Safely extract 'user' keyword argument
        super().__init__(*args, **kwargs)

        # Only filter Mavericks if the user argument is passed
        if user:
            self.fields['maverick'].queryset = Maverick.objects.filter(user=user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = self.cleaned_data.get('status', 'draft')  # Save status (draft or published)
        if commit:
            instance.save()  # Save the post instance
        return instance


class PostEditForm(forms.ModelForm):
    """Form for editing an existing post."""

    class Meta:
        model = Post
        fields = ['title', 'content', 'image']  # Removed category and tags fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded'}),
            'content': forms.Textarea(attrs={'class': 'form-control rounded'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Ensure status is set to 'draft' or 'published' when the form is saved
        if 'status' not in self.cleaned_data:
            instance.status = 'draft'  # Default to 'draft' if status is not explicitly provided
        instance.status = self.cleaned_data.get('status', instance.status)  # Ensure the status field is set
        
        if commit:
            instance.save()  # Save the post instance
        return instance
