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
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin123'  # You can change this
                )
                logging.info("✅ Superuser 'admin' created.")
            else:
                logging.info("ℹ️ Superuser 'admin' already exists.")
        except Exception as e:
            logging.error(f"❌ Error creating superuser: {e}")