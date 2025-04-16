from django.apps import AppConfig


class VarvitabelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'varvitabel'


#create superuser
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class MyAppConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        self.create_superuser()

    def create_superuser(self):
        try:
            # Check if superuser exists already
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',  # Replace with your email
                    password='admin'  # Replace with your password
                )
        except ObjectDoesNotExist:
            pass  # If any issues occur while creating, just pass