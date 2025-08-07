from django.apps import AppConfig


class TransactionsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions_app'
    
    def ready(self):
        from transactions_app import signals