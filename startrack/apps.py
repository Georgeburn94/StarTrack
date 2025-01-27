from django.apps import AppConfig

class StartrackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'startrack'

    def ready(self):
        import startrack.signals