from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text',)
        labels = {
            'text' : False
        }
        widgets = {
            'text' : forms.Textarea(attrs={'placeholder':"What's happening?", 'class': 'form-control', 'id': 'post-form', 'rows':2}) 
        }