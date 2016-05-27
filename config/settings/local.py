from .common import *

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

INTERNAL_IPS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db/app.db'),
    }
}

THIRD_PARTY_APPS += (
    'django-debug-toolbar',
)
