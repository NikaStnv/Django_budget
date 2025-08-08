from django.urls import path
from mixins_app.views import MixinDelete



urlpatterns = [
    path('<int:pk>/file_delete/', MixinDelete.as_view(), name='file_delete'),
]