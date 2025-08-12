from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from transactions_app.models import Transaction
from mixins_app.mixins import SoftDeleteMixin, StrictAuthMixin, UserFilterMixin, UserFormMixin, FilterFiniceStatsMixin
from mixins_app.mixins import LockedFieldsMixin, ExcludeDeletedMixin, LastWeekFilterMixin, SuccessMessageMixin, FiniceStatsMixin


class TransactionListView(StrictAuthMixin, UserFilterMixin, ExcludeDeletedMixin,  ListView):
    model = Transaction
    template_name = 'transactions/transactions_list.html'
    context_object_name = 'transactions'
 
    def get_queryset(self):
        return super().get_queryset().order_by('-transaction_date')


class TransactionCreateView(StrictAuthMixin, UserFormMixin, CreateView):
    model = Transaction
    fields = ['amount', 'type_transaction', 'transaction_date', 'description', 'is_planned', 'transaction_document']  
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



class TransactionSoftDeleteView(LoginRequiredMixin, SoftDeleteMixin, DeleteView):
    model = Transaction
    template_name = 'transactions/transactions_confirm_delete.html'
    success_url = reverse_lazy('list')


class TransactionDetailView(FilterFiniceStatsMixin, DetailView):
    model = Transaction
    template_name = 'transactions/transactions_details.html'
    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user,
            is_deleted=False)



