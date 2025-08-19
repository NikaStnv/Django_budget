from rest_framework import serializers
from transactions_app.models import Clients, Transaction


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    clients = ClientsSerializer(read_only=True)
    clients_id = serializers.PrimaryKeyRelatedField(
        queryset=Clients.objects.all(), source='clients', write_only=True
    )
    
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'type_transaction', 'clients', 'clients_id', 'is_deleted']