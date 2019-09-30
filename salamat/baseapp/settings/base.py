"""
Django settings for project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
SRC_ROOT = os.path.join(os.path.dirname(__file__), '..', '..')

PROJECT_ROOT = os.path.join(SRC_ROOT, '..', '..')

LANGUAGE_CODE = 'ru'

LANGUAGES = (
    ('ru', 'Russian'),
    # ('en', 'English'),
)

SITE_ID = 1

ADMINS = (
    ('maskenov', 'maskenovmn@gmail.com'),
)

MANAGERS = (
    ('Manager', 'info@tc-salamat.kz'),
    ('Manager', 'tc-salamat@yandex.ru'),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$xclt0d(6-5%#uk%+on6*@8z4iv29g7ena-^=r(pwht7ee)_)l'

# Application definition

INSTALLED_APPS = (
    # 'djangocms_admin_style',
    'modeltranslation',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.humanize',

    'sekizai',
    'cms',
    'menus',
    'treebeard',

    'djangocms_link',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    'djangocms_googlemap',
    # 'djangocms_snippet',
    'djangocms_style',
    # 'djangocms_column',
    'djangocms_text_ckeditor',
    # 'djangocms_slick_slider.apps.DjangocmsSlickSliderConfig',
    'filer',
    'easy_thumbnails',
    'mptt',
    'captcha',
    # 'cmsplugin_feedback',
    # 'meta',
    # 'djangocms_page_meta',
    'haystack',
    'aldryn_common',
    'aldryn_search',
    'standard_form',
    'spurl',
    'crispy_forms',

    'guardian',
    'userena',
    'registration',


    'django_assets',

    'filesoup',

    'baseapp',

    'customers',
    'news',
    'rents',
    'catalog',
    'projects',
    'sliders',
    'brands',
    'notifications',

)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_assets.finders.AssetsFinder',
)

STATICFILES_DIRS = [
    os.path.join(SRC_ROOT, 'baseapp', 'static'),
]

MIDDLEWARE_CLASSES = [
    # 'django.middleware.cache.UpdateCacheMiddleware',
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
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

# CRISPY
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# AUTH

LOGIN_URL = '/auth/signin/'
LOGIN_REDIRECT_URL = '/me/'
LOGIN_ERROR_URL = '/auth/signin/error/'
LOGOUT_URL = '/auth/signout/'

# USERENA

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)
ANONYMOUS_USER_ID = -1

AUTH_PROFILE_MODULE = 'customers.Customer'

USERENA_SIGNIN_REDIRECT_URL = '/accounts/%(username)s/'

USERENA_HIDE_EMAIL = True
USERENA_WITHOUT_USERNAMES = True
USERENA_SIGNIN_REDIRECT_URL = LOGIN_REDIRECT_URL
USERENA_REDIRECT_ON_SIGNOUT = '/'
USERENA_USE_MESSAGES = False
# USERENA_DEFAULT_PRIVACY = 'open'
USERENA_SIGNIN_AFTER_SIGNUP = True
USERENA_MUGSHOT_SIZE = 200
# END USERENA

WSGI_APPLICATION = 'baseapp.wsgi.application'
#
# TEMPLATE_CONTEXT_PROCESSORS = [
#     'django.contrib.auth.context_processors.auth',
#     'django.contrib.messages.context_processors.messages',
#     'django.core.context_processors.i18n',
#     'django.core.context_processors.debug',
#     'django.core.context_processors.request',
#
#     'django.core.context_processors.media',
#     'django.core.context_processors.csrf',
#     'django.core.context_processors.tz',
#     'sekizai.context_processors.sekizai',
#     'django.core.context_processors.static',
#     'cms.context_processors.cms_settings'
# ]

TEMPLATES = [{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(SRC_ROOT, 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors':
                (
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.csrf',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                ),
            'builtins': [
                # 'baseapp.templatetags.baseapp_tags',
                'customers.templatetags.customers_tags',
            ],
        }
    },
]

#
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )
#
# TEMPLATE_DIRS = (
#     os.path.join(SRC_ROOT, 'templates'),
# )

FILE_UPLOAD_PERMISSIONS = 0664


TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# THUMBNAILS

THUMBNAIL_BASEDIR = 'thumbs'
THUMBNAIL_PRESERVE_EXTENSIONS = True
THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)


FILESOUP_PROCESSORS = (
    'filesoup.processors.SimpleImageResizer',
)


LOCALE_PATHS = (
    os.path.join(SRC_ROOT, 'templates', 'locale'),
    os.path.join(SRC_ROOT, 'baseapp', 'locale'),
)


CMS_TEMPLATES = (
    ('index.html', 'Index'),
    ('aboutus.html', 'About'),
    ('contacts.html', 'Contacts'),
    ('plan.html', 'Plan'),
)

CMS_LANGUAGES = {
    'default': {
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': True,
    },
    1: [
        {
            'public': True,
            'code': 'ru',
            'hide_untranslated': False,
            'name': 'ru',
            'redirect_on_fallback': True,
        },
        # {
        #     'public': True,
        #     'code': 'en',
        #     'hide_untranslated': False,
        #     'name': 'en',
        #     'redirect_on_fallback': True,
        # },
    ],
    2: [
        {
            'public': True,
            'code': 'ru',
            'hide_untranslated': False,
            'name': 'ru',
            'redirect_on_fallback': True,
        },
        # {
        #     'public': True,
        #     'code': 'en',
        #     'hide_untranslated': False,
        #     'name': 'en',
        #     'redirect_on_fallback': True,
        # },
    ],
}

CMS_PERMISSION = False


CMS_CACHE_DURATIONS = {
    'content': 60,
    'menus': 3600,
    'permissions':3600
}

CMS_CACHE_PREFIX = "salamat"

CKEDITOR_SETTINGS = {
    'autoParagraph': False
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'KEY_PREFIX': CMS_CACHE_PREFIX,

    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'KEY_PREFIX': CMS_CACHE_PREFIX,
    }
}


# META

META_SITE_PROTOCOL = 'http'
META_USE_SITES = True
META_USE_OG_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
# META_IMAGE_URL = '/static/'


# DJANGO HAYSTACK

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'var', 'whoosh_index'),
    },
    'ru': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'var', 'whoosh_index'),
    },
    'en': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(PROJECT_ROOT, 'var',  'whoosh_index2'),

    },

}

HAYSTACK_ROUTERS = ['aldryn_search.router.LanguageRouter',]
ALDRYN_SEARCH_REGISTER_APPHOOK = True

ALDRYN_SEARCH_PAGINATION = 20