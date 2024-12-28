#backend\posts\forms.py
from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'file']  # Fields for creating a post


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']  # Fields for editing an existing post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only the content field is required

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content.strip():
            raise forms.ValidationError("Comment content cannot be empty.")
        return content

    def save(self, commit=True, parent=None):
        comment = super().save(commit=False)
        if parent:
            comment.parent = parent  # Assign the parent if it's a reply
        if commit:
            comment.save()
        return comment

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Only allow editing of the content field

    def clean_content(self):
        content = self.cleaned_data.get('content')
        
        # Optional: You can validate the content here if needed
        if not content.strip():
            raise forms.ValidationError("Comment content cannot be empty.")
        
        return content
