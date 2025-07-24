from ninja import ModelSchema, Schema
from django import forms
from transactions_app.models import Transaction
from datetime import datetime
from pydantic import ConfigDict, Field


class TransactionForm(ModelSchema):
    def validate_amount(self, value):
        if value <= 0:
            raise forms.ValidationError("Сума має бути більше 0")
        return value

    class Meta:
        model = Transaction
        fields = ['type_transaction', 'amount', 'description']


class TransactionUpdate(ModelSchema):
    def validate_amount(self, value):
        if value <= 0:
            raise forms.ValidationError("Сума має бути більше 0")
        return value

    class Meta:
        model = Transaction
        fields = ['type_transaction', 'amount', 'description']


class TransactionOut(ModelSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Meta:
        model = Transaction
        fields = '__all__'
