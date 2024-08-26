from django.apps import AppConfig

class RelojFichadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.reloj_fichador'

    def ready(self):
        import apps.reloj_fichador.signals  # Importar el archivo signals
