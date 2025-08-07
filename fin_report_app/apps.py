from django.apps import AppConfig


class FinReportAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fin_report_app'

    # def ready(self):
    #     import fin_report_app.signals  # noqa: F401
