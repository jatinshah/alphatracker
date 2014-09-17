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
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4dl-hnd+jv%&phc36coztinvzhg7ucw5_6t8#e=lrx0ufc^0+i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '127.0.0.1:8000', 'localhost:8000', '*']
ALLOWED_HOSTS = []

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
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'allauth',
    'allauth.account',
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
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'alphatracker.urls'

WSGI_APPLICATION = 'alphatracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alphatracker',
        'USER': 'django_login',
        'PASSWORD': 'dj@ng0',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
# DATABASES = {}
# DATABASES['default'] = dj_database_url.config()
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

SITE_ID = 3

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
LOGIN_REDIRECT_URL = '/c/recent/'  # TODO: Change this home page
LOGIN_URL = '/accounts/login/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Django AllAuth Settings
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USERNAME_BLACKLIST = ['edit', 'follow']
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_SESSION_REMEMBER = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
