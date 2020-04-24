from .common import *

SECRET_KEY = 'change-me'

DEBUG = True

ALLOWED_HOSTS = []

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
DEFAULT_TO_EMAIL = ''
EMAIL_ADMIN_ACCOUNT = ''

RECAPTCHA_SECRET_KEY = ''