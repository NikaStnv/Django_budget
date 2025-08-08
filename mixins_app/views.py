from django.views.generic import DetailView
from mixins_app.models import MixinsModel
from django.urls import reverse_lazy
from mixins_app.mixins import SoftDeleteMixin





# Create your views here.

class MixinDelete(SoftDeleteMixin, DetailView):
    model = MixinsModel 
    success_url = reverse_lazy('index')
    template_name = "mixins_app/mixinsmodel_confirm_delete.html"
    template_name_field = None  # Не требуется, если используете явный template_name
    # template_name_suffix = "_confirm_delete"  # Стандартный суффикс для DeleteView
