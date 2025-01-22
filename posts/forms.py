#BragiApp\posts\forms.py
from django import forms
from .models import Post
from maverick.models import Maverick  # Import Maverick model to use in the form
from filters.models import Category, Tag

class PostForm(forms.ModelForm):
    """Form for creating or editing a post."""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control rounded'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

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

            # Save tags (many-to-many field)
            instance.tags.set(self.cleaned_data['tags'])

        return instance


class PostEditForm(forms.ModelForm):
    """Form for editing an existing post."""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control rounded'})
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    maverick = forms.ModelChoiceField(
        queryset=Maverick.objects.all(),
        required=False,
        empty_label="Select a Maverick",
        widget=forms.Select(attrs={'class': 'form-control rounded'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags', 'maverick']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control rounded', 'placeholder': 'Write your content here...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter Mavericks by the logged-in user (if provided)
        if user:
            self.fields['maverick'].queryset = Maverick.objects.filter(user=user)

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Update the single category field
        if self.cleaned_data['category']:
            instance.category = self.cleaned_data['category']

        # Update tags (many-to-many field)
        if commit:
            instance.save()  # Save the post instance first
            instance.tags.set(self.cleaned_data['tags'])

        return instance
