
from baseapp.settings.base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'salamat',
        'USER': 'salamat',
        'PASSWORD': 'salamatPaSSwD',
        'HOST': 'localhost',
    }
}


ALLOWED_HOSTS = [u'test.tc-salamat.kz', u'www.test.tc-salamat.kz', u'static.tc-salamat.kz', u'tc-salamat.kz',
                 u'www.tc-salamat.kz', u'78.40.108.125', u'localhost', u'mail.tc-salamat.kz', u'127.0.0.1',
                 u'http://7c8727f2.ngrok.io',
                 u'https://7c8727f2.ngrok.io',
                 u'7c8727f2.ngrok.io',
                 ]

MANAGERS = (
    ('Manager', 'info@tc-salamat.kz'),
    ('Manager', 'tc-salamat@yandex.ru'),
)

# Recipients of traceback emails and other notifications.


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Almaty'

# Debugging displays nice error messages, but leaks memory. Set this to False
# on all server instances and True only for development.
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
THUMBNAIL_DEBUG = DEBUG
ASSETS_DEBUG = DEBUG
ASSETS_AUTO_BUILD = DEBUG

# Make this unique, and don't share it with anybody.  It cannot be blank.
SECRET_KEY = '$xclt0d(6-5%#uk%+on6*@8z4iv29g7ena-^=r(pwht7ee)_)l'

ROOT_URLCONF = 'baseapp.urls'

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'var', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'var', 'static')
STATIC_URL = '/static/'


THUMBOR_URL = 'http://thumb.tc-salamat.kz'  # No trailing slash.
THUMBOR_SECURITY_KEY = SECRET_KEY


MIDDLEWARE_CLASSES = [
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
]
CMS_PLUGIN_CACHE = False
CMS_PLACEHOLDER_CACHE =False
CMS_PAGE_CACHE = False

EMAIL_USE_TLS = True
EMAIL_HOST = 'mail.tc-salamat.kz'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@tc-salamat.kz'
EMAIL_HOST_PASSWORD = '1Qaz@wsx'

DEFAULT_FROM_EMAIL = 'TC Salamat <info@tc-salamat.kz>'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/srv/www/salamat/var/log/error.log',
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}