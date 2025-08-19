from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from transactions_app.models import Clients, Transaction
from drf_app.serializers import ClientsSerializer, TransactionSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from users_app.auth import JWTokenAuthentication


class ClientsViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name']



class TransactionViewSet(viewsets.ModelViewSet):
    # authentication_classes = [JWTokenAuthentication]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_at']
# Create your views here.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.query_params.get('mode') == 'hard':
            self.perform_destroy(instance)
        else:
            self.perform_soft_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_soft_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

# class TakeAuthToken(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             token, create = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key})
#         return Response({'error': 'Invalid credentials'}, status=400)



