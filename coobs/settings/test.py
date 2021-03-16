from .common import *

SECRET_KEY = 'django-tests'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'coobstest',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'