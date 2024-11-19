from django import forms
from .util import get_entry
from django.core.exceptions import ValidationError

class CreateForm(forms.Form):
    title = forms.CharField(max_length=50,label='Title', widget=forms.TextInput(attrs={'placeholder': 'Enter your title here.', 'class':'form-control form-control-sm'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your desctiption here.', 'class':'form-control'}))

    def clean_title(self):
        title = self.cleaned_data['title'] 
        is_exist = get_entry(title)
        if is_exist is not None:
            raise ValidationError('This title is exist! change that.')
        return title
    
class EditForm(forms.Form):
    title = forms.CharField(max_length=50,label='Title', widget=forms.TextInput(attrs={'placeholder': 'Enter your title here.', 'class':'form-control form-control-sm'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your desctiption here.', 'class':'form-control'}))
