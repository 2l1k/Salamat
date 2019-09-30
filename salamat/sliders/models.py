# coding=utf-8

from django.db import models

from django.utils.translation import ugettext_lazy as _


PLACE_CHOICES = ((1, u'Главная стр топ'),
                 (2, u'Галерея'),
                 (3, u'Видео'),)


class PublishedManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(
            active=True
        )


class Slider(models.Model):
    """
    A slider model.
    """

    title = models.CharField(_('title'), max_length=100)
    image = models.ImageField(_('Image'), upload_to='slider/images')
    position = models.PositiveIntegerField(_('position'), default=0)
    place = models.PositiveIntegerField(_(u'Положение'), choices=PLACE_CHOICES, default=1)
    link = models.URLField(_('link'), max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True, default='')
    active = models.BooleanField(default=True)

    clicks = models.IntegerField(default=0)

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'Слайдер')
        verbose_name_plural = _(u'Сдайдеры')
        ordering = ('position', 'id')

    def __unicode__(self):
        return self.title
