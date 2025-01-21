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

    # Include category, tags, and maverick fields for editing
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label="Select a Category")
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    maverick = forms.ModelChoiceField(queryset=Maverick.objects.all(), required=False, empty_label="Select a Maverick")

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags', 'maverick']  # Include the relevant fields
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control rounded', 'placeholder': 'Write your content here...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded'}),
        }

    def __init__(self, *args, **kwargs):
        # Safely extract 'user' keyword argument from kwargs
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter the Mavericks by the logged-in user (if provided)
        if user:
            self.fields['maverick'].queryset = Maverick.objects.filter(user=user)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Set the status to draft or published when saving the post
        if 'status' not in self.cleaned_data:
            instance.status = 'draft'  # Default to 'draft' if not provided
        
        instance.status = self.cleaned_data.get('status', instance.status)  # Ensure the status field is set
        
        if commit:
            instance.save()  # Save the post instance
        return instance
