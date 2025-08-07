from django.contrib import admin
from fin_report_app.models import FinancialReport, UploadedFiles

admin.site.register(FinancialReport)

admin.site.register(UploadedFiles)
# Register your models here.
