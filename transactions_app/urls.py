from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_app.views import ClientsViewSet, TransactionViewSet
from transactions_app.views import TransactionCreateView, TransactionListView, TransactionUpdateView, TransactionHardDeleteView
from transactions_app.views import TransactionSoftDeleteView, TransactionDetailView
from auth_app.views import TakeJWToken, TakeRefreshJWToken



router_drf = DefaultRouter()
router_drf.register(r'client', ClientsViewSet)
router_drf.register(r'transaction', TransactionViewSet)

urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name='create'),
    path('transactions_list/', TransactionListView.as_view(), name='list'),
    path('<int:pk>/transactions_update/', TransactionUpdateView.as_view(), name='update'),
    path('<int:pk>/transactions_delete/', TransactionHardDeleteView.as_view(), name='delete'),
    path('<int:pk>/transactions_delete_soft/', TransactionSoftDeleteView.as_view(), name='delete_soft'),
    path('<int:pk>/transactions_details/', TransactionDetailView.as_view(), name='details'),
    path('', include(router_drf.urls)),
    path('take_token/', TakeJWToken.as_view(), name='take_token'),
    path('take_refresh_token/', TakeRefreshJWToken.as_view(), name='take_refresh_token'),
        
]