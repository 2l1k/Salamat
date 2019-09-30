
import os
import json
import magic
import hashlib
import datetime
import functools

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import FieldFile
from django.core.files.uploadedfile import UploadedFile
from django import http
from filesoup import utils, settings


__all__ = ('crumb', 'require_content_type', 'upload_to_dir_slot_file',  'upload_to_dir_news', 'upload_to_dir_rents',
           'upload_to_dir_product', 'upload_to_dir_projects')


def crumb(iterable, step, limit=None, return_tail=False):
    """
    Yields step-sized crumbs from iterable.
    If :limit: is defined, the rest of iterable is yielded untouched.
    """
    stop = limit and (step * limit) or None
    for i in xrange(0, len(iterable), step):
        if i is stop:
            tail = iterable[i:]
            if tail and return_tail:
                yield tail
            break
        yield iterable[i:i + step]


def normalizer(fname):
    return '.'.join(map(utils.slugify, fname.split('.')))


def hasher(fname):
    parts = fname.split('.')
    parts[0] = hashlib.md5(parts[0]).hexdigest()
    return '.'.join(parts)


def crumber(fname):
    """
    Makes 4-level nested file name to prevent flooding of uploads folder.
    """
    slug = utils.slugify(fname).replace('-', '')

    # Complement string to be greater or equal 8 chars.
    while 0 < len(slug) < 8:
        slug *= 2

    crumbs = list(crumb(slug, 2, 4))
    crumbs.append(fname)
    return os.path.join(*crumbs)


def upload_to_dir(dirname, dateformat=None, normalizer=normalizer,
                  hasher=hasher, crumber=crumber, funcname=""):
    """
    Return callable for upload_to param in model fields.

    This is actually an interface to _upload_to_dir which was separated
    to be importable and pickleable.
    """
    def wrapper(obj, fname):
        return _upload_to_dir(obj, fname, dirname, dateformat, normalizer, hasher, crumber)

    wrapper.func_name = funcname
    wrapper.__name__ = funcname
    return wrapper


def _upload_to_dir(obj, fname, dirname, dateformat, normalizer, hasher,
                   crumber):
    for callback in [normalizer, hasher, crumber]:
        if callable(callback):
            fname = callback(fname)

    if dateformat:
        return os.path.join(dirname,
                            datetime.date.today().strftime(dateformat),
                            fname)
    return os.path.join(dirname, fname)


upload_to_dir_slot_file = upload_to_dir(settings.CLIPBOARD_DIR, '%Y%m%d',
                                        funcname="upload_to_dir_slot_file")

upload_to_dir_news = upload_to_dir('news/images', dateformat='%Y/%m/%d',
                                   funcname="upload_to_dir_news")

upload_to_dir_rents = upload_to_dir('rents/images', dateformat='%Y/%m/%d',
                                   funcname="upload_to_dir_rents")

upload_to_dir_product = upload_to_dir('catalog/product/images', dateformat='%Y/%m/%d',
                                      funcname="upload_to_dir_product")
upload_to_dir_projects = upload_to_dir('projects/images', dateformat='%Y/%m/%d',
                                      funcname="upload_to_dir_projects")



def json_response(request, data):
        body = json.dumps(data, cls=DjangoJSONEncoder, ensure_ascii=False)
        content_type = 'application/json'

        # Content type negotiation.
        if content_type not in request.META['HTTP_ACCEPT']:
            content_type = 'text/plain'

        response = http.HttpResponse(body, content_type=content_type)
        response['Content-Disposition'] = 'inline; filename=filesoup.json'
        return response


def require_content_type(f):
    """
    Returns file annotated with its content type.
    """
    content_type = getattr(f, 'content_type', None)

    if isinstance(f, UploadedFile) or not content_type:
        f_ = f
        if isinstance(f, FieldFile):
            f_ = f.file

        opened, pos = not f_.closed, None
        if opened and hasattr(f_, 'tell'):
            pos = f_.tell()

        if opened:
            f_.seek(0)
            content_type = magic.from_buffer(f_.read(2048), mime=True)
            f_.seek(pos or 0)
        else:
            f_.open()
            with f_:
                content_type = magic.from_buffer(f_.read(2048), mime=True)

    f.content_type = content_type
    return f
