import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from datetime import datetime, timezone
from django.conf import settings

User = get_user_model()

AUTHENTICATION_MESSAGES = {
    'INVALID_HEADER_FORMAT': 'Invalid Auth header format. Expected "Bearer <token>"',
    'USER_NOT_FOUND': 'User not found',
    'INVALID_TOKEN': 'Invalid token',
    'EXPIRED_TOKEN': 'Token is expired',
    'INVALID_ALGORITHM': 'Invalid token signature',
    'GENERAL_FAILURE': 'Authentication failed: '
}

class JWTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed(AUTHENTICATION_MESSAGES['INVALID_HEADER_FORMAT'])
        
        token = auth_header.split(' ')[1]
        try:
            # 1. Декодуємо токен 
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']  # PyJWT автоматично перевірить строк дії токену
            )
            
            # 2. Перевіряємо user_id
            user_id = payload.get('user_id')
            if not user_id:
                raise AuthenticationFailed(AUTHENTICATION_MESSAGES['USER_NOT_FOUND'])
            
            # 3. Отримеємо користувача
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed(AUTHENTICATION_MESSAGES['USER_NOT_FOUND'])
            
            # 4. Перевіряємо роль 
            if hasattr(settings, 'ALLOWED_ROLES'):
                required_role = payload.get('role')
                if required_role not in settings.ALLOWED_ROLES:
                    raise AuthenticationFailed(f'Invalid role: {required_role}')
            
            return (user, token)
        
        # 5. Обробляємо помилки JWT
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(AUTHENTICATION_MESSAGES['EXPIRED_TOKEN'])  
        except jwt.DecodeError:
            raise AuthenticationFailed(AUTHENTICATION_MESSAGES['INVALID_TOKEN'])
        except jwt.InvalidAlgorithmError:
            raise AuthenticationFailed(AUTHENTICATION_MESSAGES['INVALID_ALGORITHM'])
        except Exception as e:
            raise AuthenticationFailed(f"{AUTHENTICATION_MESSAGES['GENERAL_FAILURE']}{str(e)}")

    def authenticate_header(self, request):
        return 'Bearer realm="api"'