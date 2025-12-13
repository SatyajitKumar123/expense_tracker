from django import forms 
from django.utils import timezone 
from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description', 'payment_method']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # order categories: all except "Other" first, then "Other"
        categories = Category.objects.all().order_by('name')
        other = categories.filter(name__iexact='other')
        categories = categories.exclude(name__iexact='other')
        self.fields['category'].queryset = categories.union(other)
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater that 0.")
        return amount
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date