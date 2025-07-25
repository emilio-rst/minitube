from django import forms
from .models import Video
from interactions.models import Comment


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'youtube_embed_link']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'youtube_embed_link': forms.URLInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }

    def clean_youtube_embed_link(self):
        link = self.cleaned_data['youtube_embed_link']
        if 'youtube.com/embed/' not in link and 'youtu.be/' not in link:
            raise forms.ValidationError("Please provide a valid YouTube embed link")
        return link


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Write a comment...'
            }),
        } 