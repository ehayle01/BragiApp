#BragiApp\posts\forms.py
from django import forms
from .models import Post, Comment, Tag


class PostForm(forms.ModelForm):
    """Form for creating a new post."""
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control rounded', 'placeholder': 'Write your content here...'}),
            'category': forms.Select(attrs={'class': 'form-select rounded'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control rounded'}),  # Changed to SelectMultiple
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded'}),
        }

    def clean_tags(self):
        tags_input = self.cleaned_data.get('tags')
        # Since tags_input will be a list of Tag objects from the SelectMultiple, no need to split anything.
        return tags_input if tags_input else []  # Return tags or an empty list if none are selected

    def save(self, commit=True):
        instance = super().save(commit=False)
        # We no longer need to manually handle tags as a string
        tags = self.cleaned_data.get('tags')
        if tags:
            instance.save()  # Save the Post instance before setting tags
            instance.tags.set(tags)  # Associate the tags directly
        elif commit:
            instance.save()
        return instance


class PostEditForm(forms.ModelForm):
    """Form for editing an existing post."""
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded'}),
            'content': forms.Textarea(attrs={'class': 'form-control rounded'}),
            'category': forms.Select(attrs={'class': 'form-select rounded'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control rounded'}),  # Changed to SelectMultiple
            'image': forms.ClearableFileInput(attrs={'class': 'form-control rounded'}),
        }


class CommentForm(forms.ModelForm):
    """Form for creating a new comment."""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Write your comment here...',
                'rows': 3,
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError("Comment content cannot be empty.")
        return content

    def save(self, commit=True, parent=None):
        """Save a comment, optionally associating it with a parent comment."""
        comment = super().save(commit=False)
        if parent:
            comment.parent = parent
        if commit:
            comment.save()
        return comment


class CommentEditForm(forms.ModelForm):
    """Form for editing an existing comment."""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control rounded',
                'placeholder': 'Edit your comment...',
                'rows': 2,
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError("Comment content cannot be empty.")
        return content
