# coding=utf-8

from django.db import models
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from filesoup.helpers import upload_to_dir_rents
from baseapp.mixins import ImageURLProvidingMixin, ImageModelMixin
from baseapp.helpers import get_language


class RentManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(
            active=True
        )

BUILDING_CHOICES = ((1, u'Саламат-1'),
                    (2, u'Саламат-2'),
                    (3, u'Саламат-3'),
                    (4, u'Саламат-4'),
                    (5, u'Саламат-5'),)

RENT_CHOICES = ((1, u'Торговые площади'),
                (2, u'Сдаются в аренду'))


class Rent(ImageURLProvidingMixin, models.Model):
    """Model for rent"""
    active = models.BooleanField(_('Active'))
    category = models.SmallIntegerField(choices=RENT_CHOICES)
    area = models.SmallIntegerField(u'Площадь', help_text=u'кв.м', default=0)
    building = models.SmallIntegerField(u'Здание', choices=BUILDING_CHOICES)

    # Add new rows, start
    image = models.ImageField(_('Image'), upload_to='rents/images', default=0)
    description = models.TextField(_('Description'), blank=True, null=True)
    price = models.IntegerField(u'Цена за месяц', help_text=u'Т', default=0)
    # Add new rows, end

    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    objects = RentManager()

    @cached_property
    def images(self):
        if self.rentsimage_set.count():
            return self.rentsimage_set.all()
        else:
            return [self.image]


class RentsImage(ImageModelMixin, models.Model):
    """Model for project images"""
    rents = models.ForeignKey(Rent)
    file = models.ImageField(
        upload_to=upload_to_dir_rents)

    image_types = {
        'media': (620, 400),
        'detail': (800, 400),
    }

    def delete(self, using=None):
        super(RentsImage, self).delete(using)
        self.file.delete(save=False)

    delete.alters_data = True
