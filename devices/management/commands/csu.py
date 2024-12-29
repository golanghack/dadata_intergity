
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

from config.config import config
from config.essentials import is_docker

BASE_DIR = Path(__file__).resolve().parent.parent
if not is_docker():
    load_dotenv(Path(BASE_DIR.parent, ".env"))

class Command(BaseCommand):
    help = 'Create a superuser with credentials from environment variables'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = config.app.DJANGO_SUPERUSER_EMAIL
        username = config.app.DJANGO_SUPERUSER_USERNAME
        password = config.app.DJANGO_SUPERUSER_PASSWORD

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))