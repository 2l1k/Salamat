# coding=utf-8

from django.db import models

from django.utils.translation import ugettext_lazy as _


PLACE_CHOICES = ((1, u'Главная стр топ'),)


class PublishedManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(
            active=True
        )


class Notification(models.Model):
    """
    A notification model.
    """

    title = models.CharField(_('title'), max_length=100)
    position = models.PositiveIntegerField(_('position'), default=0)
    link = models.URLField(_('link'), max_length=255, blank=True, null=True)
    description = models.TextField()
    active = models.BooleanField(default=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'Уведоление')
        verbose_name_plural = _(u'Уведоления')
        ordering = ('position', 'id')

    def __unicode__(self):
        return self.title
