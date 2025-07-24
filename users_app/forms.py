from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class UserPermissionsForm(forms.Form):
    permissions = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        permissions = Permission.objects.all()
        self.fields['permissions'].choices = [
            (
                (perm.id, f'{perm.content_type.app_label}.{perm.codename} - {perm.name}')
                for perm in permissions.order_by('content_type__app_label', )
            )
        ]

        if user:
            user_permissions = user.user_permissions.values_list('id', flat=True)
            self.fields['permissions'].initial = user_permissions








