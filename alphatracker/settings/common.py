import os
from django.conf import global_settings
from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Application definition
AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + (
    'allauth.account.auth_backends.AuthenticationBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'allauth.account.context_processors.account',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'djrill',
    'allauth',
    'allauth.account',
    'captcha',
    'rest_framework',
    'content',
    'userprofile',
    'ranking',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'alphatracker.urls'

WSGI_APPLICATION = 'alphatracker.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

#Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'
DEFAULT_FROM_EMAIL = 'Jatin Shah <jatin@alphatracker.co>'
EMAIL_SUBJECT_PREFIX = ''

# django-allauth Settings
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_USERNAME_BLACKLIST = ['edit',
                              'follow',
                              'alphatracker',
                              'jatinshah']
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''
ACCOUNT_SIGNUP_FORM_CLASS = 'userprofile.forms.SignUpForm'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

# Django messages - Bootstrap integration
MESSAGE_TAGS = {
    messages.ERROR: 'alert alert-danger alert-dismissible'
}

# General Settings
SLUG_MAX_LENGTH = 50
MODERATORS = ()