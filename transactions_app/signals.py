from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from transactions_app.models import Transaction, Message

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
def transaction_saved(sender, instance, **kwargs): 
    if instance.pk is None:
        MessageContexProcessor().add_message(
            'success', f"Транзакція '{instance}' успішно створена."
        )
        MessageContexProcessor.upload_messages()
    else:
        MessageContexProcessor().add_message(
            'info', f"Транзакція '{instance}' оновлена."
        )
        MessageContexProcessor.upload_messages()