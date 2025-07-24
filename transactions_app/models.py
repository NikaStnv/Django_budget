from django.db import models


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_TRANSACTIONS = [(INCOME, 'Дохід'), (EXPENSE, 'Витрата')]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=10, choices=TYPE_TRANSACTIONS)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_type_transaction_display()}: {self.description} ({self.amount} грн.)"


    class Meta:
        ordering = ['-created_at']
