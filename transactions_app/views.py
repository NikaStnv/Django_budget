from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from transactions_app.models import Transaction
from mixins_app.mixins import SoftDeleteMixin, StrictAuthMixin, UserFilterMixin, UserFormMixin, FilterFiniceStatsMixin
from mixins_app.mixins import LockedFieldsMixin, ExcludeDeletedMixin, LastWeekFilterMixin, SuccessMessageMixin, FiniceStatsMixin
from django.core.exceptions import PermissionDenied


class TransactionListView(StrictAuthMixin, UserFilterMixin, ExcludeDeletedMixin,  ListView):
    model = Transaction
    template_name = 'transactions/transactions_list.html'
    context_object_name = 'transactions'
 
    # def get_queryset(self):
    #     return super().get_queryset().order_by('-transaction_date')
    def get_queryset(self):
        return super().get_queryset()
        search_name = self.request.GET.get('example_name')
        search_description = sefl.request.GET.get('example_description')
        if search_name:
            qs = qs.filter(name__icontains=search_name)
        if search_name:
            qs = qs.filter(name__icontains=search_description)
        return qs



class TransactionCreateView(StrictAuthMixin, UserFormMixin, CreateView):
    model = Transaction
    fields = ['amount', 'type_transaction', 'transaction_date', 'description', 'is_planned', 'transaction_document', 'clients']  
    template_name = 'transactions/transaction_create_form.html'
    success_url = reverse_lazy('list')


class TransactionUpdateView(LoginRequiredMixin, LockedFieldsMixin, UpdateView):
    model = Transaction
    fields = ['amount', 'type_transaction', 'transaction_date', 'description', 'is_planned', 'transaction_document', 'user']
    template_name = 'transactions/transactions_update_form.html'
    success_url = reverse_lazy('list')



class TransactionHardDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transactions_confirm_delete.html'
    success_url = reverse_lazy('list')

    def get_queryset(self):
        # Додаємо перевірку, що користувач може видаляти тільки свої транзакції
        return super().get_queryset().filter(user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        # Додаткова перевірка перед видаленням
        self.object = self.get_object()
        if self.object.user != self.request.user:
            raise PermissionDenied("Ви не можете видаляти чужі транзакції")
        return super().dispatch(request, *args, **kwargs)



class TransactionSoftDeleteView(LoginRequiredMixin, SoftDeleteMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transactions_confirm_delete.html'
    success_url = reverse_lazy('list')

    def get_queryset(self):
        # Додаємо перевірку, що користувач може видаляти тільки свої транзакції
        return super().get_queryset().filter(user=self.request.user)
    
    def dispatch(self, request, *args, **kwargs):
        # Додаткова перевірка перед видаленням
        self.object = self.get_object()
        if self.object.user != self.request.user:
            raise PermissionDenied("Ви не можете видаляти чужі транзакції")
        return super().dispatch(request, *args, **kwargs)


class TransactionDetailView(FilterFiniceStatsMixin, DetailView):
    model = Transaction
    template_name = 'transactions/transactions_details.html'
    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user,
            is_deleted=False)


