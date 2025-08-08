from django.dispatch import receiver, Signal
from fin_report_app.models import UploadedFiles
from transactions_app.signals import MessageContexProcessor


limit_signal = Signal() 

@receiver(limit_signal, sender=UploadedFiles)
def check_file_limits(sender, instance, **kwargs):
    word_limit = 2
    char_limit = 3
    if instance.word_count > word_limit:
       MessageContexProcessor().add_messag(
            level='warning',
            text=f"Файл '{instance.file_name}' перевищує ліміт слів, максимальний ліміт {word_limit} слів!"
        )
    MessageContexProcessor().upload_messages()

    if instance.char_count > char_limit:
        MessageContexProcessor().add_message(
            level='warning',
            text=f"Файл '{instance.file_name}' перевищує ліміт символів, максимальний ліміт {char_limit} символів!"
        )
    MessageContexProcessor().upload_messages()
       

     


