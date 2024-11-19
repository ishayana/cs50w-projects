from django import forms
from .models import Budget, Category, Transaction
from django.core.exceptions import ValidationError

class CreateBudgetForm(forms.Form):
    amount = forms.DecimalField(decimal_places=2, max_digits=13, widget=forms.NumberInput(attrs={'placeholder' : 'Amount'}))
    category = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder' : 'Category'}))
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type':'date'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateBudgetForm, self).__init__(*args, **kwargs)

    def clean_category(self):
        category_name = self.cleaned_data['category']
        try:
            category = Category.objects.get(name=category_name, user=self.request.user)
            raise ValidationError('This category already has a budget!')
        except Category.DoesNotExist:
            return category_name


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        exclude = ('date','user')

        widgets = {
         'name' : forms.TextInput(attrs={'placeholder' : 'Name'}),
         'amount' : forms.NumberInput(attrs={'placeholder' : 'Amount'}),
         'description' : forms.TextInput(attrs={'placeholder' : 'Description'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Category'
        self.fields['transaction_type'].choices = [('', 'Type')] + list(self.fields['transaction_type'].choices)[1:]
