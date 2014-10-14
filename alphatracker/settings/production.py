from .common import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

with open('/etc/django/secret_key') as f:
    SECRET_KEY = f.read().strip()

ALLOWED_HOSTS = ['.alphatracker.co', ]

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
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

MODERATORS += ('jatin', )

MANDRILL_API_KEY = '0YrV9hwcdA7JLY8SKdzySQ'  #Production Key

# django-recaptcha
RECAPTCHA_PUBLIC_KEY = '6LfAGvsSAAAAAB79NQSBAEH1Ws-Kwd4TUa7zhoKV'
RECAPTCHA_PRIVATE_KEY = '6LfAGvsSAAAAAEStYNNkvObgfIuk9AgA6FTK1lx4'
