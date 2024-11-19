from django import forms
from .models import Listing, Bids, Comment
from django.core.exceptions import ValidationError

class CreateListinForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not isinstance(field, forms.ImageField):
                field.widget.attrs['class'] = 'form-control'
    
    class Meta():
        model = Listing
        fields = '__all__'
        exclude = ['author', 'active']
        widgets = {
            'description' : forms.Textarea(attrs={'placeholder' : 'Enter your description here.'}),
            'title' : forms.TextInput(attrs={'placeholder' : 'Enter your title here.'}),
            'bid' : forms.NumberInput(attrs={'placeholder' : 'Bid start from...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class BidForm(forms.ModelForm):

    class Meta:
        model = Bids
        fields = ['amount']
        labels = {
            'amount' : False
        }
        widgets = {
            'amount' : forms.NumberInput(attrs={'class' : 'form-control', 'placeholder' : 'Enter amount'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text' : forms.TextInput(attrs={'class' : 'form-control col-md-11', 'placeholder': 'Write the comment...'})
        }

