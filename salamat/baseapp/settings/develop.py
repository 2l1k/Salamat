
import os

from baseapp.settings.base import *

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(PROJECT_ROOT, 'var', 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'salamat',
        'USER': 'salamat',
        'PASSWORD': 'salamatPaSSwD',
        'HOST': 'localhost',
    }
}

ALLOWED_HOSTS = [u'develop.er', u'127.0.0.1', u'0.0.0.0', u'localhost',
                 u'http://7c8727f2.ngrok.io',
                 u'https://7c8727f2.ngrok.io',
                 u'7c8727f2.ngrok.io',
                 ]

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
THUMBNAIL_DEBUG = DEBUG
ASSETS_DEBUG = not DEBUG
ASSETS_AUTO_BUILD = DEBUG

ROOT_URLCONF = 'baseapp.urls_dev'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'var', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'var', 'static')
STATIC_URL = '/static/'


THUMBOR_URL = 'http://develop.er:8001'  # No trailing slash.
THUMBOR_SECURITY_KEY = 'MY_SECURE_KEY'

MOBILE_REDIRECT_URL = 'http://develop.er:8000/'


MANAGERS = (
    ('Manager', 'maskenovmn@gmail.com'),
    ('Manager', 'kim@puzzle.kz')
)
# Email settings
EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.tc-salamat.kz'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@tc-salamat.kz'
EMAIL_HOST_PASSWORD = '1Qaz@wsx'
DEFAULT_FROM_EMAIL = 'TC Salamat <info@tc-salamat.kz>'

# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'