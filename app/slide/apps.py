from django.apps import AppConfig


class SlideConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.slide'

    def ready(self):
        """Prepares application"""
        # connect signals
        from . import signals
