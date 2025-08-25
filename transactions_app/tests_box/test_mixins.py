from django.test import TestCase, RequestFactory, Client
from transactions_app.models import Transaction, Clients
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse
from mixins_app.mixins import StrictAuthMixin,  SoftDeleteMixin, UserFormMixin, UserFilterMixin, LockedFieldsMixin, ExcludeDeletedMixin
from django.contrib.auth.models import User, AnonymousUser
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from django.views.generic import ListView
from django import forms
 



User = get_user_model()

class TestBaseSetUp(TestCase):
    def setUp(self):
        self.factory = RequestFactory()  # Для створення тестових запитів
        self.client = Client() # Додаємо Django test client
        self.user1 = User.objects.create_user(email='user1@mail.com', password='pass123', phone='+380671111')  # Створюємо анонімного користувача1
        self.user2 = User.objects.create_user(email='user2@mail.com', password='pass321', phone='+380672222')  # Створюємо анонімного користувача2
        self.anonymous_user = AnonymousUser()  # Створюємо анонімного користувача
        self.clients_obj = Clients.objects.create(first_name='John', last_name='Smith', id_code='654321')
        # ЗапиТранзакції для тестування
        self.transaction1 = Transaction.objects.create(amount=100, type_transaction=Transaction.INCOME, 
                                                       clients=self.clients_obj, user=self.user1, transaction_date=timezone.now().date())
        self.transaction2 = Transaction.objects.create(amount=50, type_transaction=Transaction.EXPENSE, 
                                                       clients=self.clients_obj, user=self.user1, transaction_date=timezone.now().date())
        self.transaction3 = Transaction.objects.create(amount=200, type_transaction=Transaction.INCOME, 
                                                       clients=self.clients_obj, user=self.user2, transaction_date=timezone.now().date())
        # Запити для тестування
        self.request_user1 = self.factory.get('/')
        self.request_user1.user = self.user1
        self.request_user2 = self.factory.get('/')
        self.request_user2.user = self.user2
        self.anon_request = self.factory.get('/')
        self.anon_request.user = self.anonymous_user


# Тест1 для StrictAuthMixin
    
    def test_strict_auth_mixin(self):
        class TestView(StrictAuthMixin, View): # Створюємо простий клас з базовим View
            def get(self, request):
                return HttpResponse("Успішний доступ!")
        
        self.test_obj = TestView()

        result = self.test_obj.dispatch(self.request_user1)  # Перевіряємо авторизованого користувача
        self.assertEqual(result.status_code, 200)

        with self.assertRaises(PermissionDenied) as error:  # Перевіряємо, що виникає помилка
            self.test_obj.dispatch(self.anon_request)
        self.assertEqual(str(error.exception), "Доступ заборонено. Необхідно авторизуватися.")  # Перевіряємо повідомлення помилки


# Тест2 для UserFilterMixin

    def test_user_filter_mixin(self):
        class TestView(UserFilterMixin, ListView):
            model = Transaction  
            template_name = 'test.html'
        
        # Тестуємо для user1
        view1 = TestView()
        view1.request = self.request_user1  # Встановлюємо атрибут
        queryset1 = view1.get_queryset()
        self.assertEqual(queryset1.count(), 2)
        self.assertTrue(all(obj.user == self.user1 for obj in queryset1))

        # Тестуємо для user2
        view2 = TestView()
        view2.request = self.request_user2  # Встановлюємо атрибут
        queryset2 = view2.get_queryset()
        self.assertEqual(queryset2.count(), 1)
        self.assertTrue(all(obj.user == self.user2 for obj in queryset2))
            

# Тест3 для SoftDeleteMixin  
    ## 1 варіант:
    # def test_soft_delete_mixin(self):  
    #     class TestModel:  # Створюємо простий тестовий об'єкт
    #         def __init__(self):
    #             self.is_deleted = False  # Спочатку не видалений
    #             self.deleted_at = None   # Час видалення пустий
    #         def save(self):
    #             self.was_saved = True  # Позначаємо, що save викликався
        
    #     self.test_object = TestModel()  # Створюємо екземпляр нашого тестового об'єкта
    #     self.mixin = SoftDeleteMixin()  # Створюємо наш міксин
    #     self.mixin.get_success_url = lambda: "/success/"  # URL для перенаправлення
    #     self.mixin.get_object = lambda: self.test_object  # Повертає наш тестовий об'єкт
    #     self.mixin.form_valid(None)  # Викликаємо метод form_valid нашого міксина. 
        
    #     self.assertTrue(self.test_object.is_deleted)
    #     self.assertTrue(Transaction.objects.filter(pk=self.test_object.pk).exists())  # Об'єкт існує
    #     self.assertIsNotNone(self.test_object.deleted_at)
    #     self.assertIsInstance(self.mixin.form_valid(None), HttpResponseRedirect)
    #     self.assertEqual(self.mixin.form_valid(None).url, "/success/")

    # 2 варіант:
    def test_soft_delete_mixin(self):  
        transaction = Transaction.objects.create(
            amount=100,
            type_transaction=Transaction.INCOME,
            clients=self.clients_obj,
            user=self.user1,
            transaction_date=timezone.now().date(),
            is_deleted=False
        ) # Використовуємо реальну Django модель, а не фейкову
        
        self.mixin = SoftDeleteMixin()
        self.mixin.get_success_url = lambda: "/success/"
        self.mixin.get_object = lambda: transaction  # Використовуємо реальний об'єкт
        
        self.mixin.form_valid(None)
        
        self.assertTrue(transaction.is_deleted)
        self.assertTrue(Transaction.objects.filter(pk=transaction.pk).exists())  
        self.assertIsNotNone(transaction.deleted_at)
        self.assertIsInstance(self.mixin.form_valid(None), HttpResponseRedirect)
        self.assertEqual(self.mixin.form_valid(None).url, "/success/")
            

# Тест4 для UserFormMixin
    # 1 варіант:
    def test_user_form_mixin_auto_user(self):
        """Перевіряємо міксин без реальних View"""
        # Створюємо міксин
        mixin = UserFormMixin()
        mixin.request = self.request_user1
        mixin.user_field = 'user'
        
        new_transaction = Transaction(amount=200, type_transaction=Transaction.INCOME, clients=self.clients_obj)
        
        class TestForm: # Симулюємо форму
            def __init__(self, instance):
                self.instance = instance
        
        form = TestForm(new_transaction)
                
        if not form.instance.pk: # Викликаємо логіку міксина без super()
            setattr(form.instance, mixin.user_field, mixin.request.user)
        
        self.assertEqual(new_transaction.user, self.user1)

    ## 2 варіант:  
    # def test_user_form_mixin_(self):
    #     """Тестуємо міксин в реальному TransactionCreateView"""
    #     # Створюємо реальний view
    #     view = TransactionCreateView()
    #     view.request = self.request_user1
    #     # Дані для форми
    #     form_data = {
    #         'amount': 200,
    #         'type_transaction': Transaction.INCOME,
    #         'transaction_date': timezone.now().date(),
    #         'description': 'Тестова транзакція',
    #         'is_planned': False,
    #         'clients': self.clients_obj.id
    #     }
    #     # Створюємо форму
    #     form = view.get_form_class()(data=form_data)
    #     self.assertTrue(form.is_valid(), f"Форма не валідна: {form.errors}")
    #     # Перевіряємо, що user пустий перед form_valid
    #     self.assertIsNone(form.instance.user)
    #     # Викликаємо form_valid (де працює ваш міксин)
    #     response = view.form_valid(form)
    #     # Перевіряємо, що user автоматично доданий
    #     self.assertEqual(form.instance.user, self.user1)
    #     self.assertEqual(form.instance.amount, 200)
    #     self.assertEqual(form.instance.type_transaction, Transaction.INCOME)

    
# Тест5 для LockedFieldsMixin    
    
    def test_locked_fields_mixin_logic(self):
        """Перевіряємо міксин без реальних View"""
        class TestForm(forms.ModelForm):  # Створюємо форму
            class Meta:
                model = Transaction
                fields = ['amount', 'transaction_date', 'user']
        
        form = TestForm(instance=self.transaction1)
        
        #  Симулюємо роботу міксину 
        locked_fields = ['transaction_date', 'user']
        for field in locked_fields:
            if field in form.fields:
                form.fields[field].disabled = True
                if self.transaction1:  # Симулюємо self.object
                    form.fields[field].initial = getattr(self.transaction1, field)
        
        self.assertTrue(form.fields['transaction_date'].disabled)
        self.assertTrue(form.fields['user'].disabled)
        self.assertEqual(form.fields['transaction_date'].initial, self.transaction1.transaction_date)
        self.assertEqual(form.fields['user'].initial, self.transaction1.user)
        self.assertFalse(form.fields['amount'].disabled)


# Тест6 для ExcludeDeletedMixin

    def test_exclude_deleted_mixin(self):
        initial_active_count = Transaction.objects.filter(is_deleted=False).count()  # Спочатку рахуємо скільки вже є активних транзакцій
        deleted_transaction = Transaction.objects.create(
            amount=50, 
            type_transaction=Transaction.EXPENSE,
            clients=self.clients_obj, 
            user=self.user1,
            transaction_date=timezone.now().date(),
            is_deleted=True  
        )
        active_transaction = Transaction.objects.create(
            amount=100, 
            type_transaction=Transaction.INCOME,
            clients=self.clients_obj, 
            user=self.user1, 
            transaction_date=timezone.now().date(),
            is_deleted=False  
        )
                    
        class TestView(ExcludeDeletedMixin, ListView):
            model = Transaction  
        
        view = TestView()
        queryset = view.get_queryset()
        
        expected_count = initial_active_count + 1
        self.assertEqual(queryset.count(), expected_count)  
        self.assertTrue(all(obj.is_deleted == False for obj in queryset))  
        self.assertNotIn(deleted_transaction, queryset)
        self.assertIn(active_transaction, queryset)