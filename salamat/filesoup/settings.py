
from django.conf import settings


CLIPBOARD_DIR = getattr(
    settings,
    'FILESOUP_CLIPBOARD_DIR',
    'uploads/clipboard')

PROCESSORS = getattr(
    settings,
    'FILESOUP_PROCESSORS',
    [])

THUMBNAILER = getattr(
    settings,
    'FILESOUP_THUMBNAILER',
    'filesoup.processors.DummyImageThumbnailer')

WIDGET = getattr(
    settings,
    'FILESOUP_WIDGET',
    'filesoup.widgets.jfu.JFUWidget')

IMAGE_CONTENT_TYPES = getattr(
    settings,
    'FILESOUP_IMAGE_CONTENT_TYPES',
    ['image/png', 'image/jpeg', 'image/gif'])


ALLOWED_CONTENT_TYPES = getattr(
    settings,
    'FILESOUP_CONTENT_TYPES',
    IMAGE_CONTENT_TYPES)
