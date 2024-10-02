from django.apps import AppConfig

class ActionLogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ActionLog'

    def ready(self):
        import ActionLog.signals 
