import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = False

gettext = lambda s: s
LANGUAGES = (
    ('es', gettext('Español')),
    ('en', gettext('English')),
)

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_rest_framework_camel_case',
    'django_rest_passwordreset',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware', # https://www.django-rest-framework.org/topics/internationalization/ we should send 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'coobs.middleware.dev_cors_middleware'
]

ROOT_URLCONF = 'coobs.urls'

ALLOWED_HOSTS = ['*']
WEB_PROTOCOL = "http"
WEB_URL = ""

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'coobs.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "api.Partner"

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale")
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

if os.environ.get('DEVELOPMENT_MODE', 'False') == 'True':
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'django_rest_framework_camel_case.render.CamelCaseJSONRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_PARSER_CLASSES': (
        'django_rest_framework_camel_case.parser.CamelCaseJSONParser',
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1)
}

# reCAPTCHA Enterprise Configuration
RECAPTCHA_VERIFY_URL = 'https://recaptchaenterprise.googleapis.com/v1/projects/{project_id}/assessments?key={api_key}'
RECAPTCHA_PROJECT_ID = 'coobs-476415'  # Google Cloud Project ID
RECAPTCHA_API_KEY = ''     # Google Cloud API Key
RECAPTCHA_SITE_KEY = '6Lc_wfgrAAAAADuYYdB51FTwU6OETYbQUEP84q9u'    # reCAPTCHA Enterprise Site Key
RECAPTCHA_SCORE_THRESHOLD = 0.5  # Minimum score to consider the request as legitimate

EMAIL_USE_TLS = True
EMAIL_BACKEND = ''
EMAIL_FROM_ACCOUNT = ''
EMAIL_TO_ADMIN = ''

DJANGO_REST_MULTITOKENAUTH_RESET_TOKEN_EXPIRY_TIME = 24 #hours

SDG_ENABLED = True
