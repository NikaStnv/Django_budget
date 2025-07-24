from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context_processors import request

from users_app.forms import UserPermissionsForm

User = get_user_model()

@login_required()
@permission_required('auth.change_permission', raise_exception=True)
def manage_user_permissions(required):
    users = User.objects.all()
    form = None
    selected_user = None
    user_id = request.GET.get('user_id')


# Create your views here.
