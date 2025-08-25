from django.test import TestCase
from transactions_app.models import Transaction, Clients
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.com', password='test')
        self.clients_obj = Clients.objects.create(first_name='Emma', last_name='Smith', id_code='123456')
        self.transaction = Transaction.objects.create(
            amount=100, 
            type_transaction=Transaction.INCOME, 
            clients=self.clients_obj, 
            transaction_date=timezone.now().date()
            )
    # Тест: створення об*єкту.
    def test_transaction_create(self):
        self.assertEqual(self.transaction.amount, 100)
        self.assertEqual(self.transaction.type_transaction, Transaction.INCOME)
        self.assertEqual(self.transaction.clients, self.clients_obj)
        self.assertIsNotNone(self.transaction.transaction_date)

    # Тест: Default значення
    def test_default_values(self):
        self.assertFalse(self.transaction.is_planned)  
        self.assertFalse(self.transaction.is_deleted)  
        self.assertIsNone(self.transaction.deleted_at)  
        self.assertIsNone(self.transaction.user)  

    # Тест: АвтоматиАвтоматичні поля
    def test_auto_fields(self):
        self.assertIsNotNone(self.transaction.created_at)
        self.assertIsNotNone(self.transaction.updated_at)

    # Тест: Необов*язкові поля
    def test_optional_fields(self):
        self.assertEqual(self.transaction.description, "")  
        self.assertFalse(self.transaction.transaction_document)  
            
    # Тест: Зв*язки
    def test_user_assignment(self):
        self.transaction.user = self.user
        self.transaction.save()
        self.assertEqual(self.transaction.user, self.user)

