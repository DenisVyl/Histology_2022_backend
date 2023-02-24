from datetime import timedelta
from .settings import *

RSYNC_SRC_PATH = '***'
RSYNC_DST_PATH = '***'

FILE_UPLOAD_TEMP_DIR = '***'

MEDIA_ROOT = '***'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost',]
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS.insert(0, 'debug_toolbar')
MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '***histology',
        'USER': 'postgres',
        'PASSWORD': '***',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
}

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(days=10)
