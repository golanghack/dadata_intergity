from django.contrib import admin

from config.config import config
from devices.forms import DeviceAdminForm
from devices.models import Device, DeviceModel


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    change_form_template = 'admin/devices/device/change_form.html'
    form = DeviceAdminForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['dadata_api_key'] = config.app.DADATA_API_KEY
        return super().change_view(
            request, object_id, form_url, extra_context
        )

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['dadata_api_key'] = config.app.DADATA_API_KEY
        return super().add_view(
            request, form_url, extra_context
        )

    class Media:
        js = (
            'admin/js/dadata_suggestions.js',
        )
        css = {
            'all': ('admin/css/dadata_suggestions.css',)
        }


@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') 
    search_fields = ('name',)  
    list_filter = ('name',) 

    class Meta:
        model = DeviceModel