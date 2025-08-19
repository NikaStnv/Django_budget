from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Clients(models.Model):
     first_name = models.CharField(max_length=100)
     last_name = models.CharField(max_length=100)
     id_code = models.CharField(max_length=10)

     def __str__(self):
         return f'{self.first_name} {self.last_name}'.strip()

       


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_TRANSACTIONS = [(INCOME, 'Дохід'), (EXPENSE, 'Витрата')]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=10, choices=TYPE_TRANSACTIONS)
    clients = models.ForeignKey(Clients, on_delete=models.CASCADE, related_name='clients')
    description = models.CharField(max_length=200, blank=True)
    transaction_date = models.DateField()
    is_planned = models.BooleanField(default=False)
    transaction_document = models.FileField(upload_to='transaction_documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    

    # @classmethod
    # def get_balance(cls, user=None):
    #     all_transactions = cls.objects.all()
    #     return Sum(all_transactions.filter(amount="income")) - Sum(all_transactions.filter(amount="expense"))
       
    #     all_transactions = all_transactions.filter(user=user)
    

    # def __str__(self):
    #     return f"{self.get_type_transaction_display()}: {self.description} ({self.amount} грн.) {self.transaction_date}"


    class Meta:
        ordering = ['transaction_date', 'amount']
        


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text  # Return first 50 characters of the message text

    class Meta:
        ordering = ['-created_at']






