from django import forms
from .models import Transaction
from datetime import datetime



class TransactionForm(forms.ModelForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сума має бути більше 0")
        return amount

    class Meta:
        model = Transaction
        fields = ['type_transaction', 'amount', 'description']
я

class TransactionUpdate(forms.ModelForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сума має бути більше 0")
        return amount

    class Meta:
        model = Transaction
        fields = ['type_transaction', 'amount', 'description']


class TransactionOut(forms.ModelForm):
    id: int
    created_at: datetime
    updated_at: datetime

    class Meta:
        model = Transaction
        fields = '__all__'
