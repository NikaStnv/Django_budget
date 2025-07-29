from django.db import models
from django.contrib.auth.models import Permission


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_TRANSACTIONS = [(INCOME, 'Дохід'), (EXPENSE, 'Витрата')]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=10, choices=TYPE_TRANSACTIONS)
    description = models.CharField(max_length=200, blank=True)
    transaction_date = models.DateField()
    is_planned = models.BooleanField(default=False)
    transaction_document = models.FileField(upload_to='transaction_documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @classmethod
    def get_balance(cls, user=None):
        all_transactions = cls.objects.all()
        return Sum(all_transactions.filter(amount="income")) - Sum(all_transactions.filter(amount="expense"))
       
        all_transactions = all_transactions.filter(user=user)
    

    def __str__(self):
        return f"{self.get_type_transaction_display()}: {self.description} ({self.amount} грн.) {self.transaction_date}"


    class Meta:
        ordering = ['transaction_date', 'amount']
