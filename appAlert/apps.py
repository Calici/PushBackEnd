from django.apps import AppConfig
from firebase_admin import credentials, messaging
from fcm_nonitication import settings  # Ensure this import is correct
import firebase_admin

class AppalertConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appAlert'

    def ready(self):
        cred = credentials.Certificate(settings.cred)
        firebase_admin.initialize_app(cred)
