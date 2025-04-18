# Generated by Django 5.1.4 on 2024-12-28 17:56

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=100)),
            ],
        ),
    ]
