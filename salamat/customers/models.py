# coding=utf-8

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.validators import MaxLengthValidator

from baseapp.helpers import get_client_ip

from userena.models import UserenaBaseProfile
from catalog.models import ProductCategory
from userena import settings as userena_settings


class PublishedManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(
            privacy='open'
        )


BUILDING_CHOICES = ((1, u'Саламат 1'),
                    (2, u'Саламат 2'),
                    (3, u'Саламат 3'),
                    (4, u'Саламат 4'),
                    (5, u'Саламат 5'),)


class Customer(UserenaBaseProfile):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    company_name = models.CharField(u'Название компании', max_length=200, blank=True, null=True, default='')
    category = models.ForeignKey(ProductCategory, verbose_name=u'Категория', null=True, default='')
    contract_number = models.CharField(max_length=200, blank=True, null=True, default='')
    phone = models.CharField(u'Номер телефона', max_length=30, blank=True, null=True, default='')
    building = models.SmallIntegerField(u'Здание', choices=BUILDING_CHOICES, blank=True, null=True)
    floor = models.CharField(max_length=10, blank=True, null=True)
    apartment = models.CharField(max_length=10, blank=True, null=True)
    whatsapp = models.CharField(u'Whatsapp', max_length=30, blank=True, null=True, default='')
    company_desc = models.TextField(blank=True, null=True, default='')
    company_slogan = models.CharField(u'Слоган компании', max_length=200, blank=True, null=True, default='')
    objects = PublishedManager()

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')

    def __unicode__(self):
        return self.user.email

    @property
    def email(self):
        return self.user.email

    @property
    def _username(self):
        # return self.user.email.split('@')[0]
        if userena_settings.USERENA_WITHOUT_USERNAMES:
            return self.user.email.split('@')[0] or self.user.username
        else:
            return self.user.username

    @property
    def username(self):
        return self._username

    @property
    def products(self):
        return self.user.product_set.filter(active=True)

    @models.permalink
    def get_absolute_url(self):
        return ('customer_detail', [self.pk,])

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def map_url(self):
        return '%s?build=%s&floor=%s&boutique=%s&pk=%s' % \
               (reverse('plan'), self.get_building_display(), self.floor, self.apartment, self.pk)

    def click_phone(self, request):
        click = {
            'customer': self,
            'ip': get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT'),
            'referrer': request.META.get('HTTP_REFERER'),
        }

        if request.user.is_authenticated():
            click['creator'] = request.user

        return ClickHistory.objects.create(**click)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     try:
#         instance.profile.save()
#     except:
#         Customer.objects.create(user=instance)


class Review(models.Model):
    active = models.BooleanField(_('Active'), default=False)
    customer = models.ForeignKey(Customer, verbose_name=u'Магазин', related_name='shop_reviews')
    title = models.CharField(_(u'Ваше имя'), max_length=200)
    rating = models.PositiveIntegerField(u'Рейтинг')
    message = models.TextField(u'Ваш отзыв')

    creator = models.ForeignKey(User, blank=True, null=True,  related_name='shop_reviews')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'Отзыв')
        verbose_name_plural = _(u'Отзывы')
        ordering = ('-date_added',)

    def __unicode__(self):
        return self.title

    @property
    def rating_range(self):
        return range(1, self.rating+1)


CLICK_TARGETS = ((1, 'Phone'),)


class ClickHistory(models.Model):
    customer = models.ForeignKey(Customer, verbose_name=u'Магазин', related_name='histories')
    creator = models.ForeignKey(User, blank=True, null=True, related_name='clicks')
    target = models.PositiveIntegerField(choices=CLICK_TARGETS, default=1)

    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(validators=[MaxLengthValidator(1000)], null=True, blank=True)
    referrer = models.URLField(null=True, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _(u'Показ номера')
        verbose_name_plural = _(u'Показы номеров')
        ordering = ('-date_added',)

    def __unicode__(self):
        return u'%s %s %s' % (self.customer, self.creator.profile if self.creator else '', self.date_added)

from registration.listeners import *