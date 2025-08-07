from django.contrib import admin
from transactions_app.models import Transaction, Message
from django import forms
from django.urls import path
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.contrib.admin.widgets import AdminFileWidget
import datetime
import csv
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.db import models


class TransactionAdminForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'type_transaction': forms.Select,
            'description': forms.TextInput(attrs={'size': 50, 'placeholder': 'Не более 200 символов'}),
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
            'is_planned': forms.CheckboxInput,
            'transaction_document': AdminFileWidget(attrs={'accept': '.pdf, .jpg, .jpeg, .png'}),  
            }

                                            
    def clean_transaction_document(self):
        document = self.cleaned_data.get('transaction_document')
        if document and not document.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            raise forms.ValidationError("Тільки PDF, JPG/JPEG, PNG файли!")
        return document
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Сума повине бути більше нуля!")
        return amount

class TransactionTypeFilter(admin.SimpleListFilter):
    title = 'Тип транзакції'
    parameter_name = 'type_transaction'

    def lookups(self, request, model_admin):
        return Transaction.TYPE_TRANSACTIONS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(type_transaction=self.value())
        return queryset 
    
class TransactionDateFilter(admin.SimpleListFilter):
    title = 'Дата транзакції'
    parameter_name = 'transaction_date'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Сьогодні'),
            ('this_week', 'Цього тижня'),
            ('this_month', 'Цього місяця'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(transaction_date__date=datetime.date.today())
        elif self.value() == 'this_week':
            return queryset.filter(transaction_date__week=datetime.date.today().isocalendar()[1])
        elif self.value() == 'this_month':
            return queryset.filter(transaction_date__month=datetime.date.today().month)
        return queryset
    
class TransactionPlannedFilter(admin.SimpleListFilter):
    title = 'Планована транзакція'
    parameter_name = 'is_planned'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Так'),
            ('no', 'Ні'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_planned=True)
        elif self.value() == 'no':
            return queryset.filter(is_planned=False)
        return queryset
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_per_page = 10
    list_display = ('amount', 'type_transaction', 'description', 'transaction_date', 'is_planned', 'document_preview',)
    list_filter = (TransactionTypeFilter, TransactionDateFilter, TransactionPlannedFilter)
    list_editable= ('is_planned', 'description',)
    search_fields = ('amount', 'description',)
    ordering = ('-created_at',)
    fieldsets = (
        ('Basic info', {
            'fields': ('amount', 'type_transaction', 'transaction_date',),
        }),
        ('Details', {
            'fields': ('is_planned', 'description',),
            'classes': ('collapse',)
        }),
        ('Document', {
            'fields': ('transaction_document',),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_planned', 'mark_as_not_planned', 'export_as_csv']
    ordered = ['-transaction_date', 'amount', 'type_transaction', 'is_planned']
    sortable_by = ['type_transaction', 'amount', 'is_planned']
    
    def document_preview(self, obj):
        if not obj.transaction_document:
             return "Немає документа"
    
        ext = obj.transaction_document.name.split('.')[-1].lower()
        if ext == 'pdf':
            return format_html('<a href="{}" target="_blank">📄 PDF</a>', obj.transaction_document.url)
        elif ext in ('jpg', 'jpeg'):
            return format_html('<a href="{}" target="_blank">🖼️ JPEG</a>', obj.transaction_document.url)
        elif ext == 'png':
            return format_html('<a href="{}" target="_blank">🖼️ PNG</a>', obj.transaction_document.url)
    document_preview.short_description = 'Document'

    def mark_as_planned(self, request, queryset):
        updated_count = queryset.update(is_planned=True)
        self.message_user(request, f"{updated_count} транзакцій позначено як плановані.")   
    mark_as_planned.short_description = "Позначити як плановані"

    def mark_as_not_planned(self, request, queryset):
        updated_count = queryset.update(is_planned=False)
        self.message_user(request, f"{updated_count} транзакцій позначено як не плановані.")    
    mark_as_not_planned.short_description = "Позначити як не плановані"

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions_expot.csv"'
        writer = csv.writer(response)
        writer.writerow(['Amount', 'Type', 'Description', 'Transaction Date', 'Is Planned'])
        for transaction in queryset:
            writer.writerow([transaction.amount, transaction.get_type_transaction_display(), transaction.description, transaction.transaction_date, transaction.is_planned])
        return response
    export_as_csv.short_description = "Експортувати як CSV"
    

    change_list_template = 'admin/transaction_change_list.html'    
    change_form_template = 'admin/transaction_change_form.html'

    class Media:
        css = {
            'all': ('admin/css/transaction_admin.css',)
        }
        js = ('admin/js/transaction_admin.js',)

        def get_urls(self):
            urls = super().get_urls()
            custom_urls = [
                path('dashboard/', self.admin_site.admin_view(self.dashboard_view)),
            ]
            return custom_urls + urls
        
    def get_finance_data(self, request):
            total_income = Transaction.objects.filter(type_transaction='income').aggregate(total=models.Sum('amount'))['total'] or 0
            total_expense = Transaction.objects.filter(type_transaction='expense').aggregate(total=models.Sum('amount'))['total'] or 0
            balance = total_income - total_expense
            current_date = datetime.date.today()
            return {
                'total_income': total_income,
                'total_expense': total_expense,
                'balance': balance,
                'current_date': current_date,
            }

    def changelist_view(self, request, extra_context=None):
            extra_context = extra_context or {}
            finance_data = self.get_finance_data(request)
            extra_context.update(finance_data)
            return super().changelist_view(request, extra_context=extra_context)
    
    def dashboard_view(self, request):
        finance_data = self.get_finance_data(request)
        context = dict(
            self.admin_site.each_context(request),
            title='Загальна інформація',
            **finance_data,
        )
        return TemplateResponse(request, 'admin/transactions_dashboard.html', context)
    
        
admin.site.register(Message)  # Register the Message model in the admin



