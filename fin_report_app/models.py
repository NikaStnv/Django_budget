from django.db import models
from transactions_app.models import Transaction
from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()

class FinancialReport(models.Model):
    start_date = models.DateField(verbose_name="Початок періоду")
    end_date = models.DateField(verbose_name="Кінець періоду")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ким створено")

    class Meta:
        verbose_name = "Фінансовий звіт"
        verbose_name_plural = "Фінансові звіти"
        ordering = ['-created_at']
        permissions = [('can_export_reports', "User can export the reports")]


    @property
    def period_income(self):
        return self._get_transaction_sum(Transaction.INCOME, self.start_date, self.end_date)

    @property
    def period_expenses(self):
        return self._get_transaction_sum(Transaction.EXPENSE, self.start_date, self.end_date)

    @property
    def period_balance(self):
        return self.period_income - self.period_expenses

    @property
    def total_income(self):
        return self._get_transaction_sum(Transaction.INCOME)

    @property
    def total_expenses(self):
        return self._get_transaction_sum(Transaction.EXPENSE)

    @property
    def total_balance(self):
        return self.total_income - self.total_expenses

    def __str__(self):
        return (f"Звіт за {self.start_date} - {self.end_date}:\n "
                f"Загальний дохід - {self.total_income}\n "
                f"Загальні витрати - {self.total_expenses}\n "
                f"Баланс за період - {self.period_balance}\n"
                f"Поточний баланс - {self.total_balance}")
