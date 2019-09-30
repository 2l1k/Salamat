
import json
import hashlib
import functools
import itertools
import collections

from django.conf.urls import include, url
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse, NoReverseMatch
from django.core.serializers.json import DjangoJSONEncoder
from django.template.context_processors import csrf
from django.core.files.uploadedfile import UploadedFile
from django.core.files.storage import default_storage
from django import http
from django.forms import (Form, formsets, model_to_dict, FileField,
                          IntegerField, HiddenInput)
from django.forms.models import (ModelForm, BaseModelFormSet,
                                 BaseInlineFormSet, modelformset_factory,
                                 inlineformset_factory)
from django.utils.translation import ugettext as _
from django.utils.encoding import force_text
from django.utils import six

from filesoup import settings, processors, helpers, utils
from filesoup.forms import UploaderField, AdminUploaderWidget
from filesoup.models import SlotFile
from filesoup.utils import classproperty, cachedproperty


__all__ = ('Uploader', 'ModelUploader', 'InlineModelUploader',
           'uploader_view')


class WidgetDefiningClass(type):
    """
    Metaclass for classes that has widget definitions.
    Provides `widget_class` to new class.
    """
    def __new__(mcls, name, bases, attrs):
        cls = super(WidgetDefiningClass, mcls).__new__(mcls, name, bases,
                                                       attrs)
        widget_class = getattr(cls, 'widget_class', None)
        widget_options = getattr(cls, 'Widget', None)

        if widget_class:
            if isinstance(widget_class, six.string_types):
                widget_class = utils.import_class(widget_class)

            widget_attrs = {}
            if widget_options:
                for attname, attr in widget_options.__dict__.items():
                    if not attname.startswith('_'):
                        widget_attrs[attname] = attr
            widget_attrs['uploader_class'] = cls
            widget_attrs['__module__'] = cls.__module__

            cls.widget_class = type(widget_class)(
                '%sWidget' % cls.__name__, (widget_class,), widget_attrs)

        return cls


class UploaderMetaclass(WidgetDefiningClass):
    """
    Metaclass for uploader.
    Primarily is used for generating urlpatterns from view
    method declarations.
    """
    def __new__(mcls, name, bases, attrs):
        for attname, attr in attrs.items():
            # Provide hand-crafted inheritance of meta info.
            if callable(attr) and not hasattr(attr, '_uploader_view'):
                # This may be a view callable that's not decorated.
                # Try to lookup its predecessors and check out if they're
                # decorated with `view` decorator.
                base_attrs = [getattr(base, attname) for base in bases
                              if hasattr(base, attname)]
                try:
                    meta = getattr(base_attrs[0], '_uploader_view')
                except (IndexError, AttributeError):
                    pass
                else:
                    # Got the view callable is being overloaded.
                    # Copy meta from it to current callable.
                    attr._uploader_view = meta.copy()

        cls = super(UploaderMetaclass, mcls).__new__(mcls, name, bases, attrs)

        # Gather view callables beginning from foremost base and
        # all the way down to this class. Also we need to remember
        # the order that views appear. This order will make
        # sense when generating urlconf - child views have to go first
        # because possibly they may declare the same url patterns
        # as their parents.
        views = collections.OrderedDict(
            (attname, attr)
            for mroclass in reversed(cls.mro())
            for attname, attr in mroclass.__dict__.items()
            if hasattr(attr, '_uploader_view'))

        def _uploader_view(view):
            """
            Return a view wrapper that creates uploader, performs checks etc.
            """
            @functools.wraps(view)
            def wrapper(request, *args, **kwargs):
                try:
                    uploader_kwargs = cls.get_init_kwargs(request, args,
                                                          kwargs)
                    uploader = cls(**uploader_kwargs)
                except:
                    return http.HttpResponseBadRequest(
                        _('Invalid upload params. Please try again.'))
                response = view(uploader, *args, **kwargs)
                if isinstance(response, http.HttpResponse):
                    return response
                return helpers.json_response(request, response)

            wrapper.__name__ = '.'.join((cls.__name__, view.__name__))
            return wrapper

        # Create urlpatterns.

        class_views = {}
        urlpatterns = []

        for view in views.values():
            view_name = view._uploader_view['name']
            class_views[view_name] = _uploader_view(view)

            urlpatterns.append(url(**{
                'regex': view._uploader_view['regex'],
                'view': class_views[view_name],
                'name': view_name,
            }))

        cls._views = class_views
        cls._urlpatterns = list(reversed(urlpatterns))  # Child views first.
        return cls


def uploader_view(regex, name=None):
    """
    Decorator for uploader views.
    It returns the same function annotated with meta info for metaclass.
    """
    def decorator(func):
        func._uploader_view = {
            'regex': regex,
            'name': name or func.__name__
        }
        return func
    return decorator


CLIPBOARD_FILE_FIELD_NAME = 'clipboard-file'


class UploaderFormSetMixin(object):
    def __init__(self, uploader, *args, **kwargs):
        self.uploader = uploader
        super(UploaderFormSetMixin, self).__init__(*args, **kwargs)

        self._has_clipboard_files = False
        for form in self.forms:
            fid = form[CLIPBOARD_FILE_FIELD_NAME].value()
            if fid:
                slot_file = uploader.get_slot_file(fid)
                if slot_file:
                    form.file_meta = uploader.get_slot_file_meta(slot_file)

                    if self.is_bound:
                        prefixed_field_name = form.add_prefix(
                            uploader.file_field_name)
                        form.files[prefixed_field_name] = \
                            uploader.get_file_for_form(slot_file)

                    self._has_clipboard_files = True
                else:
                    # TODO. Somehow ghost fid.
                    pass
            else:
                # This is not the form with clipboard file.
                del form.fields[CLIPBOARD_FILE_FIELD_NAME]
                form.file_meta = uploader.get_file_meta(form, self)

    def add_fields(self, form, index):
        super(UploaderFormSetMixin, self).add_fields(form, index)
        form.fields[CLIPBOARD_FILE_FIELD_NAME] = IntegerField(
            required=False, min_value=1, widget=HiddenInput)

    def has_changed(self):
        if self._has_clipboard_files:
            return True
        return super(UploaderFormSetMixin, self).has_changed()

    def _construct_form(self, i, **kwargs):
        kwargs.update(self.uploader.get_form_kwargs(i))
        return super(UploaderFormSetMixin, self)._construct_form(i, **kwargs)

    @property
    def empty_form(self):
        kwargs = {
            'auto_id': self.auto_id,
            'prefix': self.add_prefix('__filesoup_prefix__'),
            'empty_permitted': True
        }
        kwargs.update(self.uploader.get_form_kwargs(None))
        form = self.form(**kwargs)
        self.add_fields(form, None)
        return form


class UploaderFormSet(UploaderFormSetMixin, formsets.BaseFormSet):
    """Formset base class of uploader formsets."""


class BaseUploader(six.with_metaclass(UploaderMetaclass)):
    """
    Base uploader class.
    """
    # File settings.
    min_file_size = 1  # 1B - deny empty files.
    max_file_size = 5000000  # 5MB max.
    max_num = 10  # Up to 10 files per uploader.
    min_num = None

    # Allowed types for uploading.
    allowed_content_types = settings.ALLOWED_CONTENT_TYPES

    # Viewable in lightblox files.
    gallery_types = settings.IMAGE_CONTENT_TYPES

    # File processing options.
    processors = settings.PROCESSORS
    thumbnailer_class = settings.THUMBNAILER

    # Base class for widget.
    widget_class = settings.WIDGET

    # Upload form & formset options.
    form = type('UploadFileForm', (Form,), {'file': FileField(),
                                            '__module__': 'filesoup'})
    formset_class = UploaderFormSet
    formset_factory = staticmethod(formsets.formset_factory)

    # Upload files to. Meant to be callable if overridden.
    upload_to = None
    storage = default_storage  # Used when upload_to is callable.

    def __init__(self, request, prefix=None, namespace=None, empty=False,
                 instance=None):
        if namespace is None:
            namespace = request.path.strip('/').replace('/', '-') or '-'

        self.request = request
        self.prefix = prefix or 'uploader'
        self.namespace = namespace
        self.isempty = empty
        self.instance = instance  # Related Model instance.

        #print 'prefix:', self.prefix, self.isempty

    # Core properties.

    @classproperty
    def alias(cls):
        """
        Alias for this uploader class.
        """
        return cls.__name__.lower()

    @classproperty
    def ismultiple(cls):
        return cls.max_num is None or cls.max_num > 1

    @classproperty
    def issingle(cls):
        return not cls.ismultiple

    @classproperty
    def isrequired(cls):
        """
        Is at least one file required to be uploaded?
        This property is used when uploader is bound to form field.
        """
        return cls.min_num is not None and cls.min_num > 0

    @property
    def isvalid(self):
        return self.formset.is_valid()

    @property
    def errors(self):
        return self.formset.errors

    @cachedproperty
    def meta(self):
        """
        Meta info for uploader instance.
        """
        try:
            args = ['__namespace__', '__prefix__']
            upload_url = self.reverse('upload', args=args)
            clipboard_flush_url = self.reverse('clipboard_flush', args=args)
        except NoReverseMatch, e:
            error = ('%s\nPlease check out you hooked up %s.urls somewere in'
                     ' your urlconf.' % (e.message, self.__class__.__name__))
            raise NoReverseMatch(error)

        return {
            'class': self.__class__.__name__,
            'namespace': self.namespace,
            'prefix': self.prefix if not self.isempty else None,
            'urls': dict(upload=upload_url,
                         clipboard_flush=clipboard_flush_url),
            'csrftoken': force_text(csrf(self.request)['csrf_token']),
            'widget': self.widget.meta
        }

    @cachedproperty
    def meta_json(self):
        """
        Meta info for uploader instance in json format.
        """
        return json.dumps(self.meta, cls=DjangoJSONEncoder, ensure_ascii=False)

    def get_instance(self):
        """
        Returns related Model instance.
        """
        return self.instance

    def save(self, commit=True):
        """
        Base uploader has no idea about how to save uploaded files.
        """
        raise NotImplementedError()

    # Forms & formsets.

    @property
    def has_changed(self):
        return self.formset.has_changed()

    @cachedproperty
    def formset(self):
        """
        Returns a file formset.
        """
        return self.get_formset_class()(**self.get_formset_kwargs())

    @cachedproperty
    def file_field_name(self):
        """
        Detects target file field in a form and returns its name.
        """
        formset_class = self.get_formset_class()
        for field_name, field in formset_class.form.base_fields.items():
            if isinstance(field, FileField):
                return field_name
        raise ImproperlyConfigured('%s must have a file field.' %
                                   formset_class.form.__name__)

    def get_initial(self):
        """
        Returns the initial data to use for uploader formset.
        """
        initial = []

        for slot_file in self.slot_files:
            initial.append({CLIPBOARD_FILE_FIELD_NAME: slot_file['id']})

        return initial

    def get_form_kwargs(self, i):
        """
        Returns extra keyword arguments to pass to each form in the formset.
        """
        return {}

    def get_formset_kwargs(self):
        """
        Returns the keyword arguments for instantiating the formset.
        """
        kwargs = {
            'uploader': self,
            'data': self.request.POST or None,
            'files': self.request.FILES or None,
            'prefix': '%s-set' % self.prefix
        }

        initial = self.get_initial()
        if initial:
            kwargs['initial'] = initial

        return kwargs

    def get_formset_class(self):
        """
        Returns formset class.
        """
        return self.formset_factory(**self.get_formset_factory_kwargs())

    def get_formset_factory_kwargs(self):
        """
        Returns the keyword arguments for calling the formset factory.
        """
        return {
            'form': self.form,
            'formset': self.formset_class,
            'extra': 0,
            'max_num': self.max_num,
            'can_order': False,
            'can_delete': True,
        }

    def get_file_meta(self, form, formset):
        """
        """
        return {}

    # Views.

    @uploader_view(r'upload/$', name='upload')
    def upload_view(self):
        # import time
        # time.sleep(5)
        # assert False

        if self.isexceeded:
            return http.HttpResponse(
                _('Maximum number of files exceeded'),
                status=420)

        if not len(self.request.FILES):
            return http.HttpResponseBadRequest(
                _('Files were not uploaded. Please try again later.'))

        files = itertools.chain.from_iterable(
            self.request.FILES.getlist(k) for k in self.request.FILES)
        processed_files = []

        for f in files:
            fid = None
            fname = f.name

            if self.validate_file(f):
                f, fid, fname = self.process_file(f)

            processed_files.append(
                self.file_to_dict(f, id=fid, name=fname))

        return dict(files=processed_files)

    @uploader_view(r'clipboard/flush/$', name='clipboard_flush')
    def clipboard_flush_view(self):
        """
        Flushes clipboard.

        Used in frontend when creating uploader widgets in dynamic to ensure
        the clipboard for newly created uploader is clean.
        """
        self.slot_flush()
        return {}

    @classproperty
    def urls(cls):
        """
        An uploader urlconf.
        """
        # All work is already done in metaclass. Here we just create the root
        # pattern and hook up the result to it.
        my_url = r'(?P<uploader_namespace>[\w-]+)/(?P<uploader_prefix>[\w-]+)/'
        urlpatterns = [url(my_url, include(cls._urlpatterns))]
        return urlpatterns

    @classmethod
    def reverse(cls, view, *args, **kwargs):
        """
        A wrpapper of django's reverse to allow reverse self views.
        """
        if isinstance(view, six.string_types):
            if view in cls._views:
                return reverse(cls._views[view], *args, **kwargs)

        if getattr(view, 'im_class', None) is cls:
            meta = getattr(view, '_uploader_view', None)
            if meta:
                return reverse(cls._views[meta['name']], *args, **kwargs)

        return reverse(view, *args, **kwargs)

    @classmethod
    def get_init_kwargs(cls, request, args, kwargs):
        """
        Return kwargs for initializing uploader instances for views.
        """
        return {
            'request': request,
            'namespace': kwargs.pop('uploader_namespace'),
            'prefix': kwargs.pop('uploader_prefix'),
        }

    # File handling.

    @property
    def isexceeded(self):
        if self.max_num and len(self.slot_files) >= self.max_num:
            return True
        return False

    @cachedproperty
    def processor(self):
        if self.processors:
            return processors.Pipeline(self.request, self.processors)
        return None

    @cachedproperty
    def thumbnailer(self):
        if self.thumbnailer_class:
            return processors.Pipeline(self.request, [self.thumbnailer_class])
        return None

    @cachedproperty
    def slot_files(self):
        if self.isempty:
            return []  # Dummy uploader always has no uploaded files.
        return list(self.slot_list())

    def get_slot_file(self, fid):
        fid = force_text(fid)
        for f in self.slot_files:
            if force_text(f['id']) == fid:
                return f
        return None

    def get_slot_file_meta(self, slot_file):
        f, fid, fname = slot_file['file'], slot_file['id'], slot_file['name']
        if self.thumbnailer:
            f = self.thumbnailer.process(f)
        return self.file_to_dict(f, id=fid, name=fname)

    def get_file_for_form(self, slot_file):
        f, fname = slot_file['file'], slot_file['name']

        if callable(self.upload_to):
            # Assuming file from the slot already have the right url.
            return f

        helpers.require_content_type(f)
        return UploadedFile(f, fname, f.content_type, f.size)

    def get_file_for_slot(self, f):
        if callable(self.upload_to):
            return self.storage.save(self.upload_to(f), f)
        return f

    def validate_file(self, f):
        helpers.require_content_type(f)

        if f.content_type not in self.allowed_content_types:
            f.error = _('Filetype not allowed')
            return False

        if self.max_file_size and f.size > self.max_file_size:
            f.error = _('File is too big')
            return False

        return True

    def process_file(self, f):
        if self.processor:
            f = self.processor.process(f)

        slot_file = self.slot_add(self.get_file_for_slot(f), f.name)
        f, fid, fname = slot_file['file'], slot_file['id'], slot_file['name']

        if self.thumbnailer:
            f = self.thumbnailer.process(f)

        return f, fid, fname

    def file_to_dict(self, f, **kwargs):
        error = getattr(f, 'error', False)

        d = {
            'filename': f.name,
            'size': f.size,
        }

        if error:
            d['error'] = error
        else:
            helpers.require_content_type(f)
            d.update({
                'url': f.url,
                'thumbnail_url': getattr(f, 'thumbnail_url', None),
                #'filetype': f.content_type,
                'gallery': f.content_type in self.gallery_types
            })

        d.update(kwargs)
        return d

    # Widgets.

    @cachedproperty
    def widget(self):
        return self.widget_class(**self.get_widget_kwargs())

    def get_widget_kwargs(self):
        return {
            'uploader': self
        }

    # Form integration shortcuts.

    @classmethod
    def FormField(cls, *args, **kwargs):
        return UploaderField(cls, *args, **kwargs)

    @classmethod
    def AdminFormField(cls, *args, **kwargs):
        kwargs.setdefault('widget', AdminUploaderWidget)
        return UploaderField(cls, *args, **kwargs)


class BaseFileSlot(object):
    """
    """
    def slot_list(self):
        raise NotImplementedError()

    def slot_add(self, f, upload_name):
        """
        Adds file to slot. Returns `dict` with file info.

        :param f: File instance or path to file.
        :param upload_name: original name of uploaded file.
        """
        raise NotImplementedError()

    def slot_del(self, fid):
        raise NotImplementedError()

    def slot_flush(self):
        raise NotImplementedError()


class DBFileSlot(BaseFileSlot):
    """
    A slot that stores its files in db.
    """
    @cachedproperty
    def slot_folder(self):
        """
        A virtual folder for uploader instance where clipboard
        files are stored.
        """
        session = self.request.session
        if session.session_key is None:
            # Django >= 1.4 feature
            session.create()

        key = ':'.join(map(force_text, (self.alias, session.session_key,
                                        self.namespace, self.prefix)))
        #print 'key:', key
        return hashlib.sha256(key).hexdigest()

    def slot_list(self):
        for slot_file in SlotFile.objects.\
                filter(folder=self.slot_folder).all():
            yield model_to_dict(slot_file)

    def slot_add(self, f, upload_name):
        slot_file = SlotFile(folder=self.slot_folder, file=f, name=upload_name)
        slot_file.save()
        return model_to_dict(slot_file)

    def slot_del(self, fid):
        SlotFile.objects.get(id=fid).delete()

    def slot_flush(self):
        SlotFile.objects.filter(folder=self.slot_folder).delete()


class Uploader(BaseUploader, DBFileSlot):
    """Defult uploader that stores slot files in DB."""


class ModelUploaderFormSet(UploaderFormSetMixin, BaseModelFormSet):
    """Model uploader formset."""


class ModelUploader(Uploader):
    form = ModelForm
    formset_class = ModelUploaderFormSet
    formset_factory = staticmethod(modelformset_factory)
    model = None
    queryset = None
    formfield_callback = None
    fields = None
    exclude = None
    use_model_upload_to = False

    @property
    def upload_to(self):
        if self.use_model_upload_to:
            model = self.get_queryset().model

            # TODO: More correct getter
            upload_path = model.__dict__[self.file_field_name].field.upload_to

            def upload_to(f):
                if callable(upload_path):
                    return upload_path(None, f.name)

                # TODO
                raise NotImplementedError()

            return upload_to

        return None

    def get_formset_kwargs(self):
        kwargs = super(ModelUploader, self).get_formset_kwargs()
        kwargs['queryset'] = self.get_queryset()
        return kwargs

    def get_formset_factory_kwargs(self):
        kwargs = super(ModelUploader, self).get_formset_factory_kwargs()
        kwargs.update({
            'extra': len(self.slot_files),
            'model': self.get_queryset().model,
            'formfield_callback': self.formfield_callback,
            'fields': self.fields,
            'exclude': self.exclude
        })

        return kwargs

    def get_queryset(self):
        """
        Gets the queryset for current model working with.
        """
        if self.queryset is None:
            if self.model:
                return self.model._default_manager.all()
            else:
                raise ImproperlyConfigured(
                    "%(cls)s is missing a queryset. Define "
                    "%(cls)s.model, %(cls)s.queryset, or override "
                    "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__})

        return self.queryset._clone()

    def get_file_meta(self, form, formset):
        f = getattr(form.instance, self.file_field_name, None)
        if f:
            if self.thumbnailer:
                f = self.thumbnailer.process(f, form.instance)
            return self.file_to_dict(f)
        return {}

    def save(self, commit=True):
        """
        Saves forms associated with uploaded files.
        """
        result = self.formset.save(commit)
        if commit:
            # It's up to you to flush clipboard files if commit is False.
            self.slot_flush()
        return result


class InlineModelUploaderFormSet(UploaderFormSetMixin, BaseInlineFormSet):
    """Inline model uploader formset."""


class InlineModelUploader(ModelUploader):
    formset_class = InlineModelUploaderFormSet
    formset_factory = staticmethod(inlineformset_factory)
    parent_model = None
    fk_name = None

    def get_formset_kwargs(self):
        kwargs = super(InlineModelUploader, self).get_formset_kwargs()
        kwargs['instance'] = self.get_instance()
        return kwargs

    def get_formset_factory_kwargs(self):
        if not self.parent_model:
            raise ImproperlyConfigured(
                '%s is missing a parent model.' % self.__class__.__name__)

        kwargs = super(InlineModelUploader, self).get_formset_factory_kwargs()
        kwargs.update({
            'parent_model': self.parent_model,
            'fk_name': self.fk_name
        })

        return kwargs


# class DefaultUploadView(UploadView):
#     """
#     Default upload view with login required.
#     """
#     def post(self, *args, **kwargs):
#         if self.request.user.is_anonymous():
#             return http.HttpResponse(
#                 _('Login required in order to perform file uploads.'),
#                 status=401)
#         return super(DefaultUploadView, self).post(*args, **kwargs)
