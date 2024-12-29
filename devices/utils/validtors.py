import ipaddress

from django.core.exceptions import ValidationError


def validate_ip_address(value):
    try:
        ipaddress.ip_address(value)
    except ValueError:
        raise ValidationError('Некорректный IP-адрес')