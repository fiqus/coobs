from .common import *

SECRET_KEY = 'change-me'

DEBUG = True

ALLOWED_HOSTS = ['*']
WEB_PROTOCOL = "http"
WEB_URL = "localhost:8080"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_FROM_ACCOUNT = ''
EMAIL_TO_ADMIN = ''

RECAPTCHA_SECRET_KEY = ''