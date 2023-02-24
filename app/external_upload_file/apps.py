from django.apps import AppConfig


class MyFileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.external_upload_file'
