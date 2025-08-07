from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver, Signal
from fin_report_app.models import FinancialReport, UploadedFiles
from transactions_app.signals import MessageContexProcessor
from django.db.models.signals import post_save

limit_signal = Signal() 

@receiver(limit_signal, sender=UploadedFiles)
def check_file_limits(sender, instance, **kwargs):
    word_limit = 3
    char_limit = 5
    if instance.word_count > word_limit:
       MessageContexProcessor().add_message(
            level='warning',
            text=f"Файл '{instance.file_name}' перевищує ліміт слів, максимальний ліміт {word_limit} слів!"
        )
    if instance.char_count > char_limit:
        MessageContexProcessor().add_message(
            level='warning',
            text=f"Файл '{instance.file_name}' перевищує ліміт символів, максимальний ліміт {char_limit} символів!"
        )
        
        
@receiver(post_save, sender=FinancialReport)
def check_balance_limit(sender, instance, **kwargs):
    balance_limit = 1000
    if instance.total_balance < balance_limit:
        MessageContexProcessor().add_message(
            level='warning',
            text=f"Баланс менше встановленого мінімального ліміту {balance_limit}!"
        )

     


