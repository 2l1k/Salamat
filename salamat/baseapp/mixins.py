
from django.db.models.fields.files import ImageFieldFile
from baseapp.helpers import get_thumbnail_url, get_nophoto_url


class ImageURLProvidingMixin(object):
    """
    """
    image_types = {}
    image_attname = 'image'
    image_file_attname = 'file'

    def __getattr__(self, attname):
        prefix = '%s_' % self.image_attname if self.image_attname else ''
        if attname.startswith(prefix) and attname.endswith('_url'):
            type_ = attname[:attname.rfind('_url')].replace(prefix, '', 1)
            if type_ in self.image_types:
                # Got the url method.
                return self._get_image_url(type_)
        #raise AttributeError(attname)
        return super(ImageURLProvidingMixin, self).__getattr__(attname)

    def get_image_file(self):
        image_object = getattr(self, self.image_attname, self)
        if isinstance(image_object, ImageFieldFile):
            return image_object
        return getattr(image_object, self.image_file_attname, None)

    def _get_image_url(self, type_):
        f = self.get_image_file()
        try:
            options = self.image_types[type_][2]
        except IndexError:
            options = None
        size = self.image_types[type_][:2]
        return get_thumbnail_url(f, size, options)


class ImageModelMixin(ImageURLProvidingMixin):
    """
    """
    image_attname = ''  # self
    image_types = {
        'small': (32, 32),
        'media': (64, 64),
        'preview': (128, 128),
    }

    @property
    def url(self):
        image_file = self.get_image_file()
        return getattr(image_file, 'url', None) or get_nophoto_url()
