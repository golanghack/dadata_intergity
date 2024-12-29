# devices/forms.py
from dadata import Dadata
from django import forms
from django.core.exceptions import ValidationError

from config.config import config
from devices.models import Device
from devices.utils.validtors import validate_ip_address


class DeviceAdminForm(forms.ModelForm):
    ip_address = forms.GenericIPAddressField(
        validators=[validate_ip_address],
        help_text="Введите корректный IP-адрес"
    )

    class Meta:
        model = Device
        fields = '__all__'

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address:
            try:
                with Dadata(config.app.DADATA_API_KEY, config.app.DADATA_SECRET_KEY) as dadata:
                    suggestions = dadata.suggest("address", address)
                    if suggestions:
                        return suggestions[0]['value']
                    else:
                        raise ValidationError('Адрес не найден.')
            except Exception as e:
                raise ValidationError(f'Ошибка при проверке адреса: {str(e)}')
        return address

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data.get('address')
        if address:
            try:
                cleaned_data['address'] = self.clean_address()
            except ValidationError as e:
                self.add_error('address', e)
        return cleaned_data