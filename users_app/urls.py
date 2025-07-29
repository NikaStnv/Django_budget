from django.urls import path
from users_app.views import manage_user_permissions, check_permissions

# This file is part of the users_app URL configuration.
# URL configuration for users_app
urlpatterns = [
      path('manage-permissions/', manage_user_permissions, name='manage_user_permissions'), 
      path('check-permissions/', check_permissions, name='check_permissions'),
]
