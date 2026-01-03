from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os
import logging

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        
        # ONLY reads from Render Environment Variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        # Fail gracefully if env vars missing (security)
        if not all([username, password]):
            self.stdout.write(self.style.WARNING('Superuser env vars not set'))
            return
            
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} exists'))
