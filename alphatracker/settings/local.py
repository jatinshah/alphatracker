from .common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = '4dl-hnd+jv%&phc36coztinvzhg7ucw5_6t8#e=lrx0ufc^0+i'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
database_login = 'django_login'
database_password = 'dj@ang0'
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

MODERATORS += ('jatinshah', )

MANDRILL_API_KEY = '_6CAnHl3xL06uGxo05NXWg'  #Test Key

# django-recaptcha
RECAPTCHA_PUBLIC_KEY = '6Lcp-foSAAAAAEjDkUCE73FB3r-cdERqKnCEqOEQ'
RECAPTCHA_PRIVATE_KEY = '6Lcp-foSAAAAAJoXXdEbLrcbZ49HNwdocmplZuMb'
