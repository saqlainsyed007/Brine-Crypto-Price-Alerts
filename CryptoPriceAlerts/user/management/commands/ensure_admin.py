import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class Command(BaseCommand):

    def handle(self, *args, **options):

        User = get_user_model()

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")

        try:
            User.objects.create_superuser(
                username=username, password=password, email=email,
            )
            print(f"Super User Created Successfully. Username: {username} and Password: {password}.")
        except IntegrityError:
            print(f"Super User with username {username} already exists.")
