from django.apps import AppConfig


class GramoneyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GRAMONEY'

    def ready(self):
        import GRAMONEY.signals
