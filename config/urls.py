"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.template.defaultfilters import title
from django.urls import path, include
from ninja import NinjaAPI
from transactions_app.api.routers import router
from users_app.views import manage_user_permissions

api = NinjaAPI(title='Budget API', version='1.0', docs_url='/docs/')

api.add_router('/', router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('permissions/manage_permissions/', manage_user_permissions),
    path('permissions/', include('users_app.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)