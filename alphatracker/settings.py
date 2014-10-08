"""
Django settings for alphatracker project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.conf import global_settings
from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = '4dl-hnd+jv%&phc36coztinvzhg7ucw5_6t8#e=lrx0ufc^0+i'
else:
    with open('/etc/django/secret_key') as f:
        SECRET_KEY = f.read().strip()

if not DEBUG:
    ALLOWED_HOSTS = ['.alphatracker.co', ]

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


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
if DEBUG:
    database_login = 'django_login'
    database_password = 'dj@ang0'
else:
    with open('/etc/django/postgres_secret') as f:
        lines = f.read().splitlines()
        database_login = lines[0].strip()
        database_password = lines[1].strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alphatracker',
        'USER': database_login,
        'PASSWORD': database_password,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

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

CONTENT_URL = '/c/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

#Security
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Admins
ADMINS = (('Jatin Shah', 'jatindshah@gmail.com'), )
MANAGERS = ADMINS
if DEBUG:
    MODERATORS = ('jatinshah', )
else:
    MODERATORS = ('jatin')

# Email Settings
if DEBUG:
    MANDRILL_API_KEY = '_6CAnHl3xL06uGxo05NXWg'  #Test Key
else:
    MANDRILL_API_KEY = '0YrV9hwcdA7JLY8SKdzySQ'  #Production Key
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

# django-recaptcha
if DEBUG:
    RECAPTCHA_PUBLIC_KEY = '6Lcp-foSAAAAAEjDkUCE73FB3r-cdERqKnCEqOEQ'
    RECAPTCHA_PRIVATE_KEY = '6Lcp-foSAAAAAJoXXdEbLrcbZ49HNwdocmplZuMb'
else:
    RECAPTCHA_PUBLIC_KEY = '6LfAGvsSAAAAAB79NQSBAEH1Ws-Kwd4TUa7zhoKV'
    RECAPTCHA_PRIVATE_KEY = '6LfAGvsSAAAAAEStYNNkvObgfIuk9AgA6FTK1lx4'

# Django messages - Bootstrap integration
MESSAGE_TAGS = {
    messages.ERROR: 'alert alert-danger alert-dismissible'
}

# General Settings
SLUG_MAX_LENGTH = 50