from django.apps import AppConfig


class UserloginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userlogin'

    def ready(self):
        import userlogin.signals
