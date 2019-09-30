"""
File-like objects processing.
"""
import os
import operator
import mimetypes

from django.conf import settings
from django.core.files import File
from django.utils.encoding import force_unicode
from django.utils import six

from filesoup.helpers import require_content_type
from filesoup.utils import import_class


class Processor(object):
    """
    File processor.
    """
    def __init__(self, request):
        self.request = request

    def process(self, f, instance=None):
        require_content_type(f)
        type_group, type_name = f.content_type.split('/')
        type_name = type_name.replace('-', '_').replace('.', '_')

        methods = [
            # Insert process_{type_group}_{type} named method.
            '_'.join(['process', type_group, type_name]),
            # Insert process_{type_group} named method.
            '_'.join(['process', type_group]),
            # Fall back to default method if available.
            'default'
        ]

        for method in methods:
            if callable(getattr(self, method, None)):
                result = getattr(self, method)(f, instance)
                if isinstance(result, File):
                    return result
        return f


class Pipeline(object):
    def __init__(self, request, processors):
        self.processors = []
        for processor in processors:
            if isinstance(processor, six.string_types):
                processor = import_class(processor)
            self.processors.append(processor(request))

    def process(self, f, instance=None):
        for processor in self.processors:
            f = processor.process(f, instance)
        return f


class SimpleImageResizer(Processor):
    """
    Uses PIL to resize images of size gt specified.
    """
    size = (1600, 1600)

    def __init__(self, request):
        super(SimpleImageResizer, self).__init__(request)
        try:
            from PIL import Image, ImageFilter
        except ImportError:
            import Image, ImageFilter
        self.core = Image
        self.filter = ImageFilter

    def process_image(self, f, instance):
        f.open()
        im = self.core.open(f)

        if any(map(operator.gt, im.size, self.size)):
            # Need resizing.
            im.thumbnail(self.size, self.core.ANTIALIAS)
            im = im.filter(self.filter.DETAIL)
            stream = six.StringIO()
            format = 'PNG' if f.content_type.endswith('png') else 'JPEG'
            im.save(stream, format)
            f = File(stream, f.name)

        return f


class IconThumbnailer(Processor):
    """
    Thumbnailer that assigns thumbnail_url of icon matching the given
    content type of a file.
    """
    known_extensions = set([
        'accdb',
        'avi',
        'bmp',
        'css',
        'docx',
        'eml',
        'eps',
        'fla',
        'gif',
        'html',
        'ind',
        'ini',
        'jpeg',
        'jsf',
        'midi',
        'mov',
        'mp3',
        'mpeg',
        'pdf',
        'png',
        'pptx',
        'proj',
        'psd',
        'pst',
        'pub',
        'rar',
        'tiff',
        'url',
        'vsd',
        'wav',
        'wma',
        'wmv',
        'xlsx',
        'zip'])

    icons_url = settings.STATIC_URL + '/'.join(('filesoup', 'icons'))

    def default(self, f, instance):
        icon = self.get_icon_for_ext(self.get_ext(f))
        f.thumbnail_url = '/'.join((self.icons_url, icon))

    def get_ext(self, f):
        exts = mimetypes.guess_all_extensions(f.content_type)
        basename, ext = os.path.splitext(f.name)
        exts.append(ext)
        exts = (unicode.replace(force_unicode(ext), '.', '') for ext in exts)
        found = list(set(exts) & self.known_extensions)
        if len(found):
            return found[0]

    def get_icon_for_ext(self, ext):
        if ext:
            return '{0}/{0}-48_32.png'.format(ext)
        return 'text/text-48_32.png'


class DummyImageThumbnailer(IconThumbnailer):
    """
    Like IconThumbnailer but returns original file url for files
    of image type.
    """
    def process_image(self, f, instance):
        f.thumbnail_url = f.url
        return f
