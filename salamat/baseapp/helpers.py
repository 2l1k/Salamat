
import re
import json
from urlparse import urljoin

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import translation
from django.utils import six
from django.utils.functional import allow_lazy
from django.utils.encoding import force_text, iri_to_uri
from django.contrib.sites.models import Site

from django_assets.env import get_env
from libthumbor import CryptoURL
from autoslug.settings import slugify as _slugify
from pytils import translit as pytils_translit


__all__ = ('get_client_ip', 'get_assets', 'get_absolute_url', 'get_site_url',
           'get_thumbnail_url', 'get_nophoto_url', 'get_language',
           'get_default_language', 'json_dumps', 'slugify', 'safe_translify')


_absolute_url_re = re.compile(r'^https?://', re.I)
_thumbor_crypto_url = CryptoURL(settings.THUMBOR_SECURITY_KEY)


def get_client_ip(django_request_object):
    try:
        x_forwarded_for = django_request_object.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = django_request_object.META.get('REMOTE_ADDR')
    except KeyError:
        ip = '0.0.0.0'
    return ip


def get_assets(*bundle_names):
    env = get_env()
    assets = []
    for name in bundle_names:
        if name in env:
            urls = [url.replace(env.url, '', 1) for url in env[name].urls()]
            assets.extend(urls)
    return assets


def get_site_domain():
    site = Site.objects.get_current()
    return site.domain


def get_site_url(https=False):
    return get_absolute_url('', https)


def get_absolute_url(location, https=False):
    if not _absolute_url_re.match(location):
        uri = '%s://%s' % ('https' if https else 'http', get_site_domain())
        location = urljoin(uri, location)
    return iri_to_uri(location)


def get_thumbnail_url(f, size, options=None):
    url = getattr(f, 'url', None)
    if url:
        url = get_absolute_url(url)
        encrypted_url = _thumbor_crypto_url.generate(
            width=size[0], height=size[1], smart=True, image_url=url)
        return settings.THUMBOR_URL + encrypted_url
    size = 'x'.join(map(str, size))
    return '%simg/nophoto-%s.png?v=3' % (settings.STATIC_URL, size)


def add_watermark(url):
    if url:
        url = get_absolute_url(url)
        watermark_url = '%simg/watermark.png' % \
            get_absolute_url(settings.STATIC_URL)
        encrypted_url = _thumbor_crypto_url.generate(
            filters=['watermark(%s,-10,-10,50)' % watermark_url],
            image_url=url)
        return settings.THUMBOR_URL + encrypted_url


def get_nophoto_url():
    return '%simg/nophoto.png?v=3' % settings.STATIC_URL


def get_language(lang=None):
    lang = lang or translation.get_language()
    if not lang:
        return get_default_language()
    lang = lang[:2].lower()
    if not lang in get_languages():
        return get_default_language()
    return lang


def get_languages():
    return [l[0] for l in settings.LANGUAGES]


def get_default_language():
    return settings.LANGUAGE_CODE[:2].lower()


def json_dumps(data):
    return json.dumps(data, cls=DjangoJSONEncoder, ensure_ascii=False)


def slugify(value):
    return _slugify(force_text(value))
slugify = allow_lazy(slugify, six.text_type)


# @pytils_translit.returns(str)
def safe_translify(in_string):
    """
    Translify russian text.
    When string doesn't translify completely, ascii string with non-ascii
    chars ignored is returned.

    @param in_string: input string
    @type in_string: C{unicode}

    @return: transliterated string
    @rtype: C{str}
    """
    translit = force_text(in_string)
    for symb_in, symb_out in pytils_translit.TRANSTABLE:
        translit = translit.replace(symb_in, symb_out)

    try:
        translit = translit.encode('ascii', 'ignore')
    except UnicodeEncodeError:
        raise ValueError('Unicode string doesn\'t transliterate completely.')

    return translit
