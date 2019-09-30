"""
Uploader form integration.
"""
from django.core.exceptions import ValidationError
from django.forms import Field
from django.forms.forms import BoundField
from django.forms.widgets import FileInput
from django.utils import six
from django.utils.translation import ugettext as _
from filesoup import mixins



__all__ = ('UploaderFormMixin', 'UploaderField', 'UploaderWidget',
           'AdminUploaderWidget')


class UploaderFormMixin(mixins.FormWithRequestMixin):
    """
    Mixins for forms that define UploaderFields.
    """
    def __getitem__(self, name):
        """
        Returns a BoundField or UploaderBoundField with the given name.
        """
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError('Key %r not found in Form' % name)
        if isinstance(field, UploaderField):
            return UploaderBoundField(self, field, name)
        return BoundField(self, field, name)

    @property
    def media(self):
        media = super(UploaderFormMixin, self).media
        for bound_field in self:
            if isinstance(bound_field, UploaderBoundField):
                media += bound_field.uploader_media
        return media

    @property
    def uploaders(self):
        for bound_field in self:
            if isinstance(bound_field, UploaderBoundField):
                yield bound_field, bound_field.uploader

    def has_changed(self):
        """
        Returns True if data differs from initial.
        """
        for bound_field, uploader in self.uploaders:
            if uploader.has_changed:
                return True
        return super(UploaderFormMixin, self).has_changed()

    def clean(self):
        cleaned = super(UploaderFormMixin, self).clean()
        for bound_field, uploader in self.uploaders:
            if not uploader.isvalid:
                for error_dict in uploader.errors:
                    if error_dict:
                        raise ValidationError(
                            _('Some uploaded files did not validate.'))
        return cleaned

    def save(self, commit=True):
        """
        Saves a form and triggers saving of uploaded files.

        Your uploader must implement save() method in order to use this
        stuff. ``ModelUploader`` and ``InlineModelUploader`` already have
        theese methods.
        """
        result = super(UploaderFormMixin, self).save(commit)

        if commit:
            self.save_uploaded_files()
        else:
            save_m2m = getattr(self, 'save_m2m', lambda: None)

            def create_save_m2m(form):
                def new_save_m2m():
                    save_m2m()
                    form.save_uploaded_files()
                return new_save_m2m

            self.save_m2m = create_save_m2m(self)

        return result

    def save_uploaded_files(self, commit=True):
        for bound_field in self:
            if isinstance(bound_field, UploaderBoundField):
                bound_field.uploader.save(commit)

    def create_uploader(self, uploader_class, bound_field):
        """
        Creates uploader bound to a field.
        """
        # Create uploaders cache if not exists.
        self.__dict__.setdefault('_filesoup_uploaders', {})

        # Check uploader instance is already present in cache,
        # and create it if not exists.
        uploader = self._filesoup_uploaders.get(bound_field.name)
        if not uploader:
            uploader = uploader_class(**self.get_uploader_kwargs(
                                      uploader_class, bound_field))
            self._filesoup_uploaders[bound_field.name] = uploader

        # In templates, where uploader.meta might be accessed for the first
        # time, exceptions are obscured. So access meta here explicitly
        # in order to reveal exceptions caused of somehow improperly
        # configured uploader.
        uploader.meta
        return uploader

    def get_uploader_kwargs(self, uploader_class, bound_field):
        prefix = self.add_prefix(bound_field.name)
        kwargs = dict(request=self.request, prefix=prefix,
                      instance=getattr(self, 'instance', None))

        if isinstance(prefix, six.string_types):
            if '__prefix__' in prefix:
                # We are called from inside an empty form so create
                # an empty uploader.
                kwargs['empty'] = True

        return kwargs


class UploaderWidget(FileInput):
    """
    Default uploader widget.
    """


class AdminUploaderWidget(UploaderWidget):
    """
    An uploader widget for admin site forms.
    This is just a conventional subclass of UploaderWidget.
    """


class UploaderField(Field):
    """
    """
    widget = UploaderWidget

    def __init__(self, uploader_class, *args, **kwargs):
        super(UploaderField, self).__init__(*args, **kwargs)
        self.uploader_class = uploader_class
        self.required = uploader_class.isrequired


class UploaderBoundField(BoundField):
    """
    Bound field that holds uploader instance.
    """
    def as_widget(self, widget=None, attrs=None, only_initial=False):
        if attrs is None:
            attrs = {}

        if self.uploader.ismultiple:
            attrs['multiple'] = 'multiple'

        html = super(UploaderBoundField, self).as_widget(
            widget, attrs, only_initial)

        return self.uploader.widget.render(html)

    @property
    def uploader(self):
        return self.form.create_uploader(self.field.uploader_class, self)

    @property
    def uploader_media(self):
        if isinstance(self.field.widget, AdminUploaderWidget):
            return self.uploader.widget.admin_media
        return self.uploader.widget.media
