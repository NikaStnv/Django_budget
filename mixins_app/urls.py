from django.urls import path
from mixins_app.views import HardDelete, SoftDelete



urlpatterns = [
    path('<int:pk>/file_delete/', HardDelete.as_view(), name='file_delete'),
    path('<int:pk>/file_delete_soft/', SoftDelete.as_view(), name='file_delete_soft'),
]