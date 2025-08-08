from django.db.models.signals import post_save, pre_save
from transactions_app.models import Transaction, Message
from fin_report_app.models import FinancialReport
from django.dispatch import receiver

class MessageContexProcessor:
    _messages = []

    def add_message(self, level, text):
        self._messages.append({'level': level, 'text': text})

    @classmethod
    def get_messages(cls):
        messages = cls._messages
        cls._messages.clear()
        return messages
    
    @classmethod
    def upload_messages(cls):
            for message in cls._messages:
                Message.objects.create(text=message['text'])
            cls._messages.clear()

        

@receiver(post_save, sender=Transaction)
def transaction_saved(sender, instance, created, **kwargs): 
    if created:
        MessageContexProcessor().add_message(
            'success', f"Транзакція '{instance}' успішно створена."
        )
        MessageContexProcessor.upload_messages()
    else:
        MessageContexProcessor().add_message(
            'info', f"Транзакція '{instance}' оновлена."
        )
        MessageContexProcessor.upload_messages()

        

# @receiver(post_save, FinancialReport)
# def check_balance_limit(sender, instance, **kwargs):
#     balance_limit = 1000
        
#     if instance.total_balance < balance_limit:
#         MessageContexProcessor().add_message(
#             level='warning',
#             text=f"Баланс менше встановленого мінімального ліміту {balance_limit}!"
#         )
#         MessageContexProcessor.upload_messages()