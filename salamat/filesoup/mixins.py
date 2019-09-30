"""
Filesoup uploader heavily relies on current request.
This collection of mixins is called to ease integration of uploader
into your app.
"""

from django.utils.functional import curry
from django.core.exceptions import ImproperlyConfigured


class FormWithRequestMixin(object):
    """
    A mixin to Form with a `request` attribute.
    """
    def __init__(self, *args, **kwargs):
        try:
            self.request = kwargs.pop('request')
        except KeyError:
            raise ImproperlyConfigured('Please provide a request to %s '
                                       'instance' % self.__class__.__name__)
        super(FormWithRequestMixin, self).__init__(*args, **kwargs)


class RequestProvidingFormViewMixin(object):
    """
    A mixin to View that provides `request` kwarg to a form instance.
    """
    def get_form_kwargs(self):
        kwargs = super(RequestProvidingFormViewMixin, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


# For admin site.

class RequestProvidingModelAdminMixin(object):
    """
    A mixin for ModelAdmin and InlineModelAdmin classes to provide `request`
    kwarg to underlying forms.
    """
    def get_form(self, request, obj=None, **kwargs):
        form_class = super(RequestProvidingModelAdminMixin, self).\
            get_form(request, obj, **kwargs)
        form_class.__init__ = curry(form_class.__init__, request=request)
        return form_class

    def get_formset(self, request, obj=None, **kwargs):
        formset = super(RequestProvidingModelAdminMixin, self).\
            get_formset(request, obj, **kwargs)
        formset.form.__init__ = curry(formset.form.__init__, request=request)
        return formset
