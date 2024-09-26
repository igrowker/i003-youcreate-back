from django.apps import AppConfig

class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name'  # Cambia esto por el nombre de tu aplicación

    def ready(self):
        import your_app_name.signals  # Asegúrate de importar el archivo signals
