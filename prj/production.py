from .settings import *

# DEBUG = False

RSYNC_SRC_PATH = '***'
RSYNC_DST_PATH = '***'

FILE_UPLOAD_TEMP_DIR = '***'
MEDIA_ROOT = '***'


ALLOWED_HOSTS = ['***.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '***histology',
        'USER': 'postgres',
        'PASSWORD': '***',
        'HOST': '***',
        'PORT': '5432',
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}

STATIC_URL = '/static_dj/'
STATIC_ROOT = BASE_DIR / 'static/'
