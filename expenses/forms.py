from django import forms
from django.utils import timezone
from django.db.models import Case, When, Value, IntegerField

from .models import Expense, Category


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description', 'payment_method']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['category'].queryset = (
            Category.objects.annotate(
                is_other=Case(
                    When(name__iexact='other', then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).order_by('is_other', 'name')
        )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return amount

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise forms.ValidationError("Date cannot be in the future.")
        return date
