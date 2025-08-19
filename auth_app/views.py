import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import AllowAny
from datetime import datetime, timezone
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


USER_ROLES = {
    'DEFAULT': 'visitor',
    'ADMIN': 'admin',
    'STAFF': 'user'
}
ERROR_MESSAGES = {
    'CREDENTIALS_REQUIRED': 'Email and password are required',
    'INVALID_CREDENTIALS': 'Invalid credentials!',
    'REFRESH_TOKEN_REQUIRED': 'Refresh token is required!',
    'INVALID_REFRESH_TOKEN': 'Invalid refresh token!',
    'USER_NOT_FOUND': 'User not found'
}

class TakeJWToken(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': ERROR_MESSAGES['CREDENTIALS_REQUIRED']}, status=400)

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': ERROR_MESSAGES['INVALID_CREDENTIALS']}, status=400)
        
        role = USER_ROLES['DEFAULT']
        if user.is_superuser:
            role = USER_ROLES['ADMIN']
        elif user.is_staff:
            role = USER_ROLES['STAFF']

        token_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
        token_payload = {
            'user_id': user.id,
            'exp': datetime.now(timezone.utc) + token_lifetime,
            'iat': datetime.now(timezone.utc)
        }
        
        access_payload = token_payload.copy()
        access_payload.update({
            'email': user.email,
            'role': role
        })

        refresh_lifetime = settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')
        refresh_payload = token_payload.copy()
        refresh_payload.update({
            'type': 'refresh',
            'exp': datetime.now(timezone.utc) + refresh_lifetime,
            'email': user.email,    
            'role': role
        })

        access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')

        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {'id': user.id, 'email': user.email, 'role': role}
        })


class TakeRefreshJWToken(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': ERROR_MESSAGES['REFRESH_TOKEN_REQUIRED']}, status=400)
        
        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            if payload.get('type') != 'refresh':
                return Response({'error': ERROR_MESSAGES['INVALID_REFRESH_TOKEN']}, status=400)

            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed(ERROR_MESSAGES['USER_NOT_FOUND'])
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed(ERROR_MESSAGES['USER_NOT_FOUND'])
            
            role = USER_ROLES['DEFAULT']
            if user.is_superuser:
                role = USER_ROLES['ADMIN']
            elif user.is_staff:
                role = USER_ROLES['STAFF']

            token_lifetime = settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
            token_payload = {
                'user_id': user.id,
                'exp': datetime.now(timezone.utc) + token_lifetime,
                'iat': datetime.now(timezone.utc)
            }
            
            access_payload = token_payload.copy()
            access_payload.update({
                'email': user.email,
                'role': role
            })

            refresh_token_payload = token_payload.copy()
            refresh_token_payload.update({
                'type': 'refresh',
                'exp': datetime.now(timezone.utc) + settings.SIMPLE_JWT.get('REFRESH_TOKEN_LIFETIME')
            })

            access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
            new_refresh_token = jwt.encode(refresh_token_payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({
                'access_token': access_token,
                'refresh_token': new_refresh_token,
                'user': {'id': user.id, 'email': user.email, 'role': role}
            })
            
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Refresh token is expired'}, status=400)
        except jwt.DecodeError:
            return Response({'error': 'Invalid refresh token'}, status=400)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid refresh signature'}, status=400)