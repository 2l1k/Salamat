
import urlparse

from django import forms
from django.conf import settings
from django.utils.encoding import smart_unicode

from baseapp.helpers import get_assets, get_language, json_dumps


__all__ = ('RedactorWidget', 'TreeNodeChoiceField')


class TreeNodeChoiceField(forms.ModelChoiceField):
    """Duplicating the TreeNodeChoiceField bundled in django-mptt
    to avoid conflict with the TreeNodeChoiceField bundled in django-cms..."""
    def __init__(self, level_indicator=u'|--', *args, **kwargs):
        self.level_indicator = level_indicator
        if kwargs.get('required', True) and not 'empty_label' in kwargs:
            kwargs['empty_label'] = None
        super(TreeNodeChoiceField, self).__init__(*args, **kwargs)

    def label_from_instance(self, obj):
        """Creates labels which represent the tree level of each node
        when generating option labels."""
        return u'%s %s' % (self.level_indicator * getattr(
            obj, obj._mptt_meta.level_attr), smart_unicode(obj))


class RedactorWidget(forms.Textarea):
    """
    A Redactor.js widget.

    Additional kwargs:

    ``options`` - a dictionary of named settings and values.
    See the Redactor `API docs <http://redactorjs.com/docs/settings>`_ for
    available settings.

    Example usage::

        >>> RedactorWidget(
                options={
                    'lang': 'en',
                    'iframe': True,
                    'css': 'styles/style.css'
                }
            )
    """
    def __init__(self, attrs=None, options=None):
        super(RedactorWidget, self).__init__(attrs=attrs)

        defaults = {
            'buttons': [
                'html', '|', 'formatting', '|',
                'bold', 'italic', 'deleted', '|',
                'horizontalrule', '|',
                'image', 'video', 'file', 'table', 'link', '|',
                'unorderedlist', 'orderedlist', 'outdent', 'indent', '|',
                'alignment']
        }

        if options:
            defaults.update(options)
        self.options = defaults

        if 'css' in self.options:
            self.options['css'] = self.build_url(self.options['css'])

    def build_url(self, path):
        if any(map(path.startswith, ['http://', 'https://', '/'])):
            return path
        else:
            prefix = settings.STATIC_URL or settings.MEDIA_URL
            return urlparse.urljoin(prefix, path)

    @property
    def media(self):
        js = get_assets('redactor_js')
        js2 = []
        for s in js:
            js2.append(s.split('?', 1)[0])
        css = get_assets('redactor_css')
        css2 = []
        for s in css:
            css2.append(s.split('?', 1)[0])
        css = dict(screen=css2)
        return forms.Media(js=js2, css=css)

    def render(self, name, value, attrs=None):
        css_class = attrs.get('class', 'redactor-textarea')
        if 'redactor-textarea' not in css_class:
            css_class += ' redactor-textarea'
        attrs['class'] = css_class
        self.options.setdefault('lang', get_language())
        attrs['data-redactor-meta'] = json_dumps(self.options)
        return super(RedactorWidget, self).render(name, value, attrs)


class MessageForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField()
    subject = forms.CharField(max_length=100, required=False)
