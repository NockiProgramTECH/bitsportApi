from django.apps import AppConfig


class MarketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.markets'
    label = 'markets'
    verbose_name = 'Marchés'

    def ready(self):
        # On importe les signaux ici pour qu'ils soient enregistrés
        import apps.markets.signals
