from django.apps import AppConfig


class AssociatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'associates'

    def ready(self):
        import associates.signals