
from django.core.exceptions import ImproperlyConfigured
from django.forms import Media, MediaDefiningClass
from django.template.response import SimpleTemplateResponse
from django.utils.safestring import mark_safe
from django.utils import six

__all__ = ('UploaderWidget',)


class ExtraMediaDefiningClass(MediaDefiningClass):
    """
    For classes that can have Media + AdminMedia definitions.
    """
    def __new__(mcls, name, bases, attrs):
        cls = super(ExtraMediaDefiningClass, mcls).__new__(mcls, name, bases,
                                                           attrs)
        if 'admin_media' not in attrs:
            # Construct admin media property.
            def media(self):
                # Get the media property of the superclass, if it exists.
                media = getattr(super(cls, self), 'admin_media', Media())

                # Get the media definition for this class
                definition = getattr(cls, 'AdminMedia', None)

                if not definition:
                    return media

                extend = getattr(definition, 'extend', True)
                if extend:
                    if extend is True:
                        m = media
                    else:
                        m = Media()
                        for medium in extend:
                            m = m + media[medium]
                    return m + Media(definition)
                else:
                    return Media(definition)

            cls.admin_media = property(media)

        return cls


class UploaderWidget(six.with_metaclass(ExtraMediaDefiningClass)):
    """
    Base class for uploader widget.
    """
    # An uploader class holding this widget. Set automatically.
    uploader_class = None
    template_name = None  # Main widget template.

    def __init__(self, uploader):
        self.uploader = uploader

    def __unicode__(self):
        return self.render()

    @property
    def meta(self):
        """
        Widget meta info propagated to frontend.
        """
        return {}

    def get_context_data(self):
        return dict(uploader=self.uploader, widget=self)

    def get_template_names(self):
        """
        Returns a list of template names to be used for widget rendering.
        Must return a list.
        """
        if self.template_name is None:
            raise ImproperlyConfigured(
                "Widget requires either a definition of 'template_name' "
                "or an implementation of 'get_template_names()'")
        return [self.template_name]

    def render(self, file_input_html=''):
        """
        Renders widget.

        :file_input_html: may come from rendered form field uploader
        is bound to.
        """
        self.file_input_html = file_input_html or self.get_file_input_html()
        content = SimpleTemplateResponse(
            self.get_template_names(), self.get_context_data())
        return content.rendered_content

    def get_file_input_html(self):
        attrs = 'name="%s"' % self.uploader.prefix
        if self.uploader.ismultiple:
            attrs += ' multiple="multiple"'
        return mark_safe('<input type="file" %s />' % attrs)
