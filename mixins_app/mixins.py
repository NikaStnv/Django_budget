from django.utils import timezone
from django.http import HttpResponseRedirect



class SoftDeleteMixin:
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object = self.get_object()
        self.object.s_deleted = True
        self.object.deleted_at = timezone.now()
        self.object.save()
        return HttpResponseRedirect(success_url)