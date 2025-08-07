from ninja import Router
from django.shortcuts import get_object_or_404
from typing import List
from transactions_app.models import Transaction
from .schemas import TransactionForm, TransactionUpdate, TransactionOut


router = Router(tags=["Transactions"])

@router.post("", response=TransactionOut)
def create_transaction(request, payload: TransactionForm):
    return Transaction.objects.create(**payload.dict())

@router.get("", response=List[TransactionOut])
def list_transactions(request):
    return Transaction.objects.all()

@router.get("/{id}", response=TransactionOut)
def get_transaction(request, id: int):
   return get_object_or_404(Transaction, id=id)

@router.put("/{id}", response=TransactionOut)
def update_transaction(request, id: int, payload: TransactionUpdate):
    transaction = get_object_or_404(Transaction, id=id)
    for attr, value in payload.dict().items():
        setattr(transaction, attr, value)
    transaction.save()
    return transaction

@router.delete("/{id}", response={204: None})
def delete_transaction(request, id: int):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.delete()
    return 204, None