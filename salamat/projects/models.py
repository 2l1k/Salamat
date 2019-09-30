
from django.db import models
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField

from filesoup.helpers import upload_to_dir_projects
from baseapp.mixins import ImageURLProvidingMixin, ImageModelMixin
from baseapp.helpers import get_language


class ProjectManager(models.Manager):

    def published(self):
        return self.get_queryset().filter(
            active=True
        )


class Project(ImageURLProvidingMixin, models.Model):
    """Model for project"""
    title = models.CharField(_('Title'), max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=255)
    active = models.BooleanField(_('Active'))
    image = models.ImageField(
        _('Preview'),
        upload_to=upload_to_dir_projects)
    logo = models.ImageField(
        _('Logo'),
        upload_to=upload_to_dir_projects, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = ProjectManager()

    image_types = {
        'media': (620, 400),
        'detail': (800, 400),
    }

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        # translation.activate(get_language())
        return ('project_detail', [self.pk, self.slug])

    @property
    def url(self):

        return self.get_absolute_url()

    @cached_property
    def images(self):
        return self.projectimage_set.all()

    @property
    def previous_project(self):
        return self.previous_next_projects[0]

    @property
    def next_project(self):
        return self.previous_next_projects[1]

    @property
    def previous_next_projects(self):
        previous_next = getattr(self, 'previous_next', None)

        if previous_next is None:
            if not self.active:
                previous_next = (None, None)
                setattr(self, 'previous_next', previous_next)
                return previous_next

            projects = list(self.__class__.objects.published())
            index = projects.index(self)
            try:
                previous = projects[index + 1]
            except IndexError:
                previous = projects[-1]

            if index:
                _next = projects[index - 1]
            else:
                _next = projects[0]
            previous_next = (previous, _next)
            setattr(self, 'previous_next', previous_next)
        return previous_next


class ProjectImage(ImageModelMixin, models.Model):
    """Model for project images"""
    project = models.ForeignKey(Project)
    file = models.ImageField(
        upload_to=upload_to_dir_projects)

    image_types = {
        'media': (620, 400),
        'detail': (800, 400),
    }

    def delete(self, using=None):
        super(ProjectImage, self).delete(using)
        self.file.delete(save=False)

    delete.alters_data = True
