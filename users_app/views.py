from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required, permission_required
from django.template.context_processors import request
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden                                                                                                                                           
from users_app.forms import UserPermissionsForm
from django.contrib import messages

User = get_user_model()

@login_required
@permission_required('auth.change_permission', raise_exception=True)
def manage_user_permissions(request):
    users = User.objects.all()
    form = None
    selected_user = None
    user_id = request.GET.get('user_id')
  
    if request.method == 'POST':
        if user_id:= request.POST.get('user_id'):
            selected_user = get_object_or_404(User, id=user_id)
            form = UserPermissionsForm(request.POST, user=selected_user)
            if form.is_valid():
                permissions = form.cleaned_data['permissions']
                selected_user.user_permissions.set(permissions)
                selected_user.save()
            messages.success(request, f'Дозволи для {selected_user} оновлено')
            return redirect('manage_user_permissions')
        form = UserPermissionsForm(user=None)
    else:
        if user_id:= request.GET.get('user_id'):         
            selected_user = get_object_or_404(User, id=user_id)
            form = UserPermissionsForm(user=selected_user)
        else:
            form = UserPermissionsForm(user=None)
    context = {'users': users, 'form': form, 'selected_user': selected_user}
    return render(request, 'manage_user_permissions.html', context)


@login_required
@permission_required('fin_report_app.change_financialreport', raise_exception=True)
def check_permissions(request):
    return render(request, 'manage_user_permissions.html')
