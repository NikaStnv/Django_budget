from django.utils import timezone  
from django.urls import reverse
from django.test import TestCase, RequestFactory, Client  
from django.contrib.auth.models import User, AnonymousUser
from transactions_app.models import Transaction, Clients
from transactions_app.tests_box.test_mixins import TestBaseSetUp
from transactions_app.views import TransactionListView, TransactionCreateView, TransactionUpdateView
from transactions_app.views import TransactionSoftDeleteView, TransactionHardDeleteView, TransactionDetailView

class TransactionListViewTest(TestBaseSetUp):
       
    def test_view_requires_login(self):
        """Перевіряємо, що view вимагає авторизації"""
        self.client.logout()
        response = self.client.get(reverse('list'))  
        self.assertEqual(response.status_code, 403)  

    def test_view_accessible_to_logged_in_user(self):
        """Перевіряємо, що авторизований користувач має доступ"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('list'))  
        self.assertEqual(response.status_code, 200)

    def test_view_returns_only_user_transactions(self):
        """Перевіряємо, що повертаються тільки транзакції поточного користувача"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('list'))  
        
        transactions = response.context['transactions']
        self.assertEqual(len(transactions), 2)
        for transaction in transactions:
            self.assertEqual(transaction.user, self.user1)

    def test_template_used(self):
        """Перевіряємо, що використовується правильний шаблон"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('list'))  
        self.assertTemplateUsed(response, 'transactions/transactions_list.html')


class TransactionCreateViewTest(TestBaseSetUp):
        
    def test_create_view_sets_current_user(self):
        """Перевіряємо, що створена транзакція має поточного юзера"""
        self.client.force_login(self.user1)
        form_data = {
            'amount': 150,
            'type_transaction': 'income',
            'clients': self.clients_obj.id,
            'transaction_date': timezone.now().date(),
            'description': 'Test transaction'
        }
        
        response = self.client.post(reverse('create'), form_data)  
        
        self.assertEqual(response.status_code, 302)
        transaction = Transaction.objects.get(amount=150)
        self.assertEqual(transaction.user, self.user1)
        
    def test_success_url_redirect(self):
        """Перевіряємо, що після створення відбувається редірект на правильний URL"""
        self.client.force_login(self.user1)
        form_data = {
        'amount': 150,
        'type_transaction': 'income',
        'clients': self.clients_obj.id,
        'transaction_date': timezone.now().date(),
        'description': 'Test transaction'
    }
        response = self.client.post(reverse('create'), form_data)  
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list'))  


class TransactionUpdateViewTest(TestBaseSetUp):
       
    def test_locked_fields_in_update_view(self):
        """Перевіряємо, що поля заблоковані в формі редагування"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('update', kwargs={'pk': self.transaction1.pk}))        
        form = response.context['form']
        self.assertTrue(form.fields['transaction_date'].disabled)
        self.assertTrue(form.fields['user'].disabled)
        self.assertFalse(form.fields['amount'].disabled)

    def test_update_transaction(self):
        """Перевіряємо оновлення транзакції"""
        self.client.force_login(self.user1)
        form_data = {
            'amount': 999,
            'type_transaction': 'expense',
            'description': 'Updated description'
        }
        
        response = self.client.post(reverse('update', kwargs={'pk': self.transaction1.pk}), form_data)  
        
        self.transaction1.refresh_from_db()
        self.assertEqual(self.transaction1.amount, 999)
        self.assertEqual(self.transaction1.type_transaction, 'expense')
        self.assertEqual(self.transaction1.description, 'Updated description')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list'))  


class TransactionSoftDeleteViewTest(TestBaseSetUp):
        
    def test_soft_delete_sets_is_deleted(self):
        """Перевіряємо, що м'яке видалення встановлює is_deleted=True"""
        self.client.force_login(self.user1)
        self.assertFalse(self.transaction1.is_deleted)
        
        response = self.client.post(reverse('delete_soft', kwargs={'pk': self.transaction1.pk}))  
        
        self.transaction1.refresh_from_db()
        self.assertTrue(self.transaction1.is_deleted)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list'))  

    def test_cannot_soft_delete_other_user_transaction(self):
        """Перевіряємо, що не можна м'яко видалити чужу транзакцію"""
        self.client.force_login(self.user1)
        
        response = self.client.post(reverse('delete_soft', kwargs={'pk': self.transaction3.pk}))  
        
        # Якщо видалення пройшло успішно (302), перевіряємо, що об'єкт НЕ був видалений
        if response.status_code == 302:
            self.transaction3.refresh_from_db()
            self.assertFalse(self.transaction3.is_deleted)  # Перевіряємо, що не видалено
        else:
            self.assertIn(response.status_code, [403, 404])


class TransactionHardDeleteViewTest(TestBaseSetUp):
        
    def test_hard_delete_removes_object(self):
        """Перевіряємо, що жорстке видалення видаляє об'єкт з БД"""
        self.client.force_login(self.user1)
        transaction_id = self.transaction1.id
        
        response = self.client.post(reverse('delete', kwargs={'pk': self.transaction1.pk}))  
        
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(id=transaction_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('list'))  

        def test_cannot_hard_delete_other_user_transaction(self):
            """Перевіряємо, що не можна жорстко видалити чужу транзакцію"""
            self.client.force_login(self.user1)
            
            # Запам'ятовуємо ID перед спробою видалення
            transaction3_id = self.transaction3.id
            
            response = self.client.post(reverse('delete', kwargs={'pk': self.transaction3.pk}))
            
            # Перевіряємо, що транзакція все ще існує
            self.transaction3.refresh_from_db()
            self.assertEqual(self.transaction3.id, transaction3_id)
            
            # Має повернути 403 або 404
            self.assertIn(response.status_code, [403, 404])


class TransactionDetailViewTest(TestBaseSetUp):
        
    def test_cannot_view_other_user_transaction(self):
        """Перевіряємо, що не можна переглядати чужі транзакції"""
        self.client.force_login(self.user1)
        
        response = self.client.get(reverse('details', kwargs={'pk': self.transaction3.pk}))  
        
        self.assertIn(response.status_code, [403, 404])
    
    def test_can_view_own_transaction(self):
        """Перевіряємо, що можна переглядати свої транзакції"""
        self.client.force_login(self.user1)
        response = self.client.get(reverse('details', kwargs={'pk': self.transaction1.pk}))  
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object'], self.transaction1)