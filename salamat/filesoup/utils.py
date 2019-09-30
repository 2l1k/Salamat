
from django.conf import settings
from django.utils.functional import cached_property
from django.utils import six


class classproperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func(owner)


class cachedproperty(cached_property):
    """
    More concrete cached_property that can be accesible via instances only.
    """
    def __get__(self, instance, owner):
        if not instance:
            raise AttributeError("%s is accessible via %s instances only." % (
                                 self.func.__name__, owner.__name__))
        return super(cachedproperty, self).__get__(instance, owner)


def import_class(importpath):
    try:
        module, klass = importpath.rsplit('.', 1)
    except (ValueError, AttributeError):
        raise ValueError(
            '"%s" doesn\'t seem to be an import path string.' % importpath)
    try:
        module = __import__(module, fromlist=[klass])
    except ImportError as e:
        raise ImportError(
            'Failed to import class "%s" from module "%s". Reason: %s.' % (
                klass, module, e))
    try:
        klass = getattr(module, klass)
    except AttributeError:
        raise AttributeError(
            'Module "%s" does not define a "%s" class.' % (
                module.__name__, klass))

    return klass


# Make use of django-autoslug compatible slugify function.

slugify = getattr(settings, 'AUTOSLUG_SLUGIFY_FUNCTION', None)

if not slugify:
    try:
        from unidecode import unidecode
        slugify = lambda s: unidecode(s).replace(' ', '-')
    except ImportError:
        try:
            from pytils.translit import slugify
        except ImportError:
            slugify = 'django.template.defaultfilters.slugify'

if isinstance(slugify, six.string_types):
    from django.urls import get_callable
    slugify = get_callable(slugify)
