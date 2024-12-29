import uuid

from django.contrib.auth.hashers import make_password
from django.db import models


class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=False, null=False)
    password = models.CharField(max_length=100)
    def __str__(self):
        return self.username