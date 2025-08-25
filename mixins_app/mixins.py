from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.generic import DeleteView
from datetime import timedelta
from django.db.models import Sum, Q



class SoftDeleteMixin(DeleteView):
    """М'яке видалення об'єкту"""
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.deleted_at = timezone.now()
        self.object.save()
        return HttpResponseRedirect(success_url)
    

class StrictAuthMixin(LoginRequiredMixin):
    """Перевірка авторизації"""
    permission_denied_message = ("Доступ заборонено. Необхідно авторизуватися.")
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied(self.permission_denied_message)
        try:
            return super().dispatch(request, *args, **kwargs)
        except AttributeError:
            return "Успішний доступ!"


class UserFilterMixin(LoginRequiredMixin):
    """Доступ по користувачу"""
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    # def get_queryset(self):
    #     try:
    #         queryset = super().get_queryset()
    #     except AttributeError:
    #         from transactions_app.models import Transaction
    #         queryset = Transaction.objects.none()  # Пустий queryset
    #     return queryset.filter(user=self.request.user)
    

class UserFormMixin(LoginRequiredMixin):
    """Автоматичне додавання користувача при створені форми"""
    user_field = 'user'  
     
    def form_valid(self, form):
        if not form.instance.pk:  
            setattr(form.instance, self.user_field, self.request.user)
        # Перевірку наявності ф-ції form_valid в базовоому класі
        try:
            return super().form_valid(form)
        except AttributeError: # Якщо немає, повертаємо redirect
            from django.http import HttpResponseRedirect
            from django.urls import reverse_lazy
            return HttpResponseRedirect(reverse_lazy('list'))


class LockedFieldsMixin:
    """Забороняє зміни вказаних полів,  міксін призначений для використання разом з Django class-based views, особливо з UpdateView"""
    locked_fields = ['transaction_date', 'user']  # Незмінювані поля
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in self.locked_fields:
            if field in form.fields:
                # Робимо поле неактивним в формі
                form.fields[field].disabled = True
                # Фіксуєм початкове значення
                if self.object:
                    form.fields[field].initial = getattr(self.object, field)
        return form
    

class ExcludeDeletedMixin:
    """Міксин, який виключає видалені об'єкти (is_deleted=True)"""
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_deleted=False)
    

class LastWeekFilterMixin:
    """Фільтр на останні 7 днів (тиждень)"""
    def get_queryset(self):
        one_week_ago = timezone.now() - timedelta(days=7)
        return super().get_queryset().filter(
            transaction_date__gte=one_week_ago  
        ).order_by('-transaction_date')  
    

class SuccessMessageMixin:
    """Додає повідомлення про успіх після виконання операції."""
    success_message = ""

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response
    

# class ReadOnlyMixin:
#     """Міксин, що робить доступним тільки читання/перегляд"""
    
#     def dispatch(self, request, *args, **kwargs):
#         if request.method in ('GET', 'HEAD', 'OPTIONS'):
#             return super().dispatch(request, *args, **kwargs)
        
#         if request.user.is_superuser:
#             return super().dispatch(request, *args, **kwargs)
            
#         raise PermissionDenied("Зміни заборонені. У вас немає прав на редагування.")


class FiniceStatsMixin:
    """Міксін для визначення фінансових показників"""
    def get_finance_data(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            
        stats = queryset.filter(is_deleted=False).aggregate(
            income=Sum('amount', filter=Q(type_transaction='income')),
            expense=Sum('amount', filter=Q(type_transaction='expense')),
        )
        return {
            'total_income': stats.get('income') or 0,
            'total_expense': stats.get('expense') or 0,
            'balance': (stats.get('income') or 0) - (stats.get('expense') or 0),
        }
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_finance_data())
        return context
    

class FilterFiniceStatsMixin(FiniceStatsMixin):
    """Автоматично враховує фільтри з get_queryset() View."""
    def get_finance_data(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()  
        return super().get_finance_data(queryset)