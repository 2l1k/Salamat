
from django.db import models
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField

from filesoup.helpers import upload_to_dir_news
from baseapp.mixins import ImageURLProvidingMixin, ImageModelMixin
from baseapp.helpers import get_language


class NewsManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(
            active=True
        )


class News(ImageURLProvidingMixin, models.Model):
    """Model for news"""
    title = models.CharField(_('Title'), max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=255)
    image = models.ImageField(
        _('Preview'),
        upload_to=upload_to_dir_news)
    active = models.BooleanField(_('Active'))
    brief = models.TextField(_('Brief'), help_text=_('Preview text'))
    description = models.TextField(_('Description'), blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = NewsManager()

    image_types = {
        'media': (390, 250),
        'detail': (800, 400),
    }

    class Meta:
        verbose_name = _('News')
        verbose_name_plural = _('News')
        ordering = ['-date_updated']

    def __unicode__(self):
        return self.title


    @models.permalink
    def get_absolute_url(self):
        return ('news_detail', [self.pk, self.slug])

    @property
    def url(self):

        return self.get_absolute_url()

    @cached_property
    def images(self):
        if self.newsimage_set.count():
            return self.newsimage_set.all()
        else:
            return [self.image]

    @property
    def previous_news(self):
        return self.previous_next_news[0]

    @property
    def next_news(self):
        return self.previous_next_news[1]

    @property
    def previous_next_news(self):
        previous_next = getattr(self, 'previous_next', None)

        if previous_next is None:
            if not self.active:
                previous_next = (None, None)
                setattr(self, 'previous_next', previous_next)
                return previous_next

            news = list(self.__class__.objects.published())
            index = news.index(self)
            try:
                previous = news[index + 1]
            except IndexError:
                previous = news[-1]

            if index:
                _next = news[index - 1]
            else:
                _next = news[0]
            previous_next = (previous, _next)
            setattr(self, 'previous_next', previous_next)
        return previous_next


class NewsImage(ImageModelMixin, models.Model):
    """Model for project images"""
    news = models.ForeignKey(News)
    file = models.ImageField(
        upload_to=upload_to_dir_news)

    image_types = {
        'media': (620, 400),
        'detail': (800, 400),
    }

    def delete(self, using=None):
        super(NewsImage, self).delete(using)
        self.file.delete(save=False)

    delete.alters_data = True
