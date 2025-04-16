from django.apps import AppConfig


class VarvitabelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'varvitabel'




from django.contrib.auth.models import User
import logging

class VarvitabelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'varvitabel'

    def ready(self):
        from django.contrib.auth.models import User  # ✅ move import here
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin'
            )