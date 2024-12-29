from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class DeviceModel(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название модели'))
    description = models.TextField(verbose_name=_('Описание модели'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Модель устройства')
        verbose_name_plural = _('Модели устройств')
        ordering = ['name',]

class Device(models.Model):
    address = models.CharField(max_length=255, verbose_name=_('Адрес'))
    name = models.CharField(max_length=100, verbose_name=_('Название устройства'))
    ip_address = models.GenericIPAddressField(verbose_name=_('IP-адрес'))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Автор'))
    device_model = models.ForeignKey(DeviceModel, on_delete=models.SET_NULL, null=True, verbose_name=_('Модель устройства'))
    comment = models.TextField(blank=True, verbose_name=_('Комментарий'))

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

    class Meta:
        verbose_name = _('Устройство')
        verbose_name_plural = _('Устройства')
        ordering = ['name',]

