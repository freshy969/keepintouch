from django.views.generic import UpdateView

from .models import KITSystem
from .forms import SystemSettingsForm

    
    
class SystemSettingsUpdateView(UpdateView):
    
    model = KITSystem
    form_class = SystemSettingsForm
    template_name = 'gomez/system_settings.html'
    
    def get_object(self, queryset=None):
        return self.request.user.kituser.kitsystem
    
    def get_context_data(self, **kwargs):
        params = super(SystemSettingsUpdateView, self).get_context_data(**kwargs)
        params["syssetid"] = self.object.pk
        return params
    
    def get_queryset(self):
        # user should not be able to view the settings of other users
        qs = super(SystemSettingsUpdateView, self).get_queryset()
        return qs.filter(kit_admin=self.request.user.kituser)
