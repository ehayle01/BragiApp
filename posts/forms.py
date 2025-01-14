#BragiApp\posts\forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """Form for creating or editing a post."""
    
    status = forms.ChoiceField(
        choices=[('draft', 'Draft'), ('published', 'Published')],
        initial='draft',
        widget=forms.RadioSelect(),
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'image', 'status']  # Include status in the form
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control rounded', 'placeholder': 'Write your content here...'}),
            'category': forms.Select(attrs={'class': 'form-select rounded'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control rounded'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded'}),
        }

    def clean_tags(self):
        tags_input = self.cleaned_data.get('tags')
        return tags_input if tags_input else []  # Return tags or an empty list if none are selected

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = self.cleaned_data.get('status', 'draft')  # Save status (draft or published)
        if commit:
            instance.save()  # Save the post instance
            tags = self.cleaned_data.get('tags')
            if tags:
                instance.tags.set(tags)  # Associate tags if any
        return instance


class PostEditForm(forms.ModelForm):
    """Form for editing an existing post."""
    
    status = forms.ChoiceField(
        choices=[('draft', 'Draft'), ('published', 'Published')],
        required=False,  # Status will be handled in the view, so it's not strictly required here
        widget=forms.RadioSelect(),
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded'}),
            'content': forms.Textarea(attrs={'class': 'form-control rounded'}),
            'category': forms.Select(attrs={'class': 'form-select rounded'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control rounded'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded'}),
        }

    def clean_tags(self):
        tags_input = self.cleaned_data.get('tags')
        return tags_input if tags_input else []  # Return tags or an empty list if none are selected

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Ensure status is set to 'draft' or 'published' when the form is saved
        if 'status' not in self.cleaned_data:
            instance.status = 'draft'  # Default to 'draft' if status is not explicitly provided
        instance.status = self.cleaned_data.get('status', instance.status)  # Ensure the status field is set
        
        if commit:
            instance.save()  # Save the post instance
            tags = self.cleaned_data.get('tags')
            if tags:
                instance.tags.set(tags)  # Associate tags if any
        return instance
