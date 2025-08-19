from django.urls import path
from fin_report_app.views import upload_file, list_uploaded_files, view_uploaded_files, delete_uploaded_file
from fin_report_app.views import ListAndUploadView, FileDetailView


urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('files/', list_uploaded_files, name='list_uploaded_files'),
    path('files/<int:upload_file_id>/', view_uploaded_files, name='view_uploaded_files'),
    path('files/<int:upload_file_id>/delete/', delete_uploaded_file, name='delete_uploaded_file'),
    path('files_cbv/', ListAndUploadView.as_view(), name='list_uploaded_files_cbv'),
    path('files_cbv/<int:upload_file_id>/', FileDetailView.as_view(), name='view_files_cbv'),
]