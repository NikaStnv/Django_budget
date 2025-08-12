from django.urls import path
from transactions_app.views import TransactionCreateView, TransactionListView, TransactionUpdateView, TransactionHardDeleteView
from transactions_app.views import TransactionSoftDeleteView, TransactionDetailView


urlpatterns = [
    path('create/', TransactionCreateView.as_view(), name='create'),
    path('transactions_list/', TransactionListView.as_view(), name='list'),
    path('<int:pk>/transactions_update/', TransactionUpdateView.as_view(), name='update'),
    path('<int:pk>/transactions_delete/', TransactionHardDeleteView.as_view(), name='delete'),
    path('<int:pk>/transactions_delete_soft/', TransactionSoftDeleteView.as_view(), name='delete_soft'),
    path('<int:pk>/transactions_details/', TransactionDetailView.as_view(), name='details'),
    
]