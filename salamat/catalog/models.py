# coding=utf-8

from django.db import models
from django.utils import translation
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils import timezone

from autoslug import AutoSlugField

from filesoup.helpers import upload_to_dir_product
from baseapp.mixins import ImageURLProvidingMixin, ImageModelMixin
from baseapp.helpers import get_language


class PublishedManager(models.Manager):
    def published(self):
        return self.get_queryset().filter(
            active=True
        )


class ProductCategory(models.Model):
    active = models.BooleanField(_('Active'), default=True)
    title = models.CharField(_('Title'), max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=255)
    parent = models.ForeignKey('self', related_name='childs', blank=True, null=True)
    icon = models.ImageField(_('Icon white'), upload_to='catalog/category/icons', blank=True, null=True)
    icon_red = models.ImageField(_('Icon red'), upload_to='catalog/category/icons', blank=True, null=True)
    position = models.PositiveIntegerField(_('position'), default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'Категория')
        verbose_name_plural = _(u'Категории')
        ordering = ('position', 'id')

    def __unicode__(self):
        if self.parent:
            return u'%s-%s' % (self.parent, self.title)
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('category_detail', [self.pk, self.slug, ])

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def path(self):
        s = ''
        if self.parent:
            if self.parent.parent:
                s = '%s-' % self.parent.parent.title
            s += self.parent.title + '-'
        s += self.title
        return s

    @property
    def tags(self):
        s = ''
        if self.parent:
            if self.parent.parent:
                s = '%s, %s, ' % (self.parent.parent.title, self.parent.parent.slug)
            s += self.parent.title + ', ' + self.parent.slug + ', '
        s += self.title + ', ' + self.slug
        return s

    @property
    def root(self):
        if self.parent:
            if self.parent.parent:
                return self.parent.parent
            return self.parent
        return self


class ProductType(models.Model):
    active = models.BooleanField(_('Active'), default=True)
    title = models.CharField(_('Title'), max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'Тип товара')
        verbose_name_plural = _(u'Типы товара')

    def __unicode__(self):
        return self.title


STOCK_CHOICES = ((1, u'В наличии'),
                 (2, u'Нет в наличии'),
                 (3, u'Под заказ'),
                 (4, u'Ожидается'),)

DISCOUNT_CHOICES = ((1, u'%'),
                    (2, u'тг'),)


class Product(models.Model):
    """Model for product"""

    category = models.ForeignKey(ProductCategory, verbose_name=u'Категория')
    product_type = models.ForeignKey(ProductType, verbose_name=u'Тип', blank=True, null=True)

    title = models.CharField(_(u'Наименование товара'), max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=255)

    description = models.TextField(_(u'Описание товара'), blank=True, null=True, default='')
    price_from = models.BooleanField(_(u'Установить цену от'), default=False)
    price = models.PositiveIntegerField(_(u'Цена'), blank=True, null=True)
    quantity = models.PositiveIntegerField(u'Количество', blank=True, null=True)
    stock = models.PositiveIntegerField(_(u'В наличии'), choices=STOCK_CHOICES, default=1)
    brand = models.CharField(_(u'Бренд'), max_length=200, blank=True, null=True, default='')
    collection = models.CharField(_(u'Коллекция'), max_length=200, blank=True, null=True, default='')
    color = models.CharField(_(u'Цвет'), max_length=200, blank=True, null=True, default='')

    active = models.BooleanField(_('Active'), default=True)
    featured = models.BooleanField(_('Featured'), default=False)

    seo_title = models.TextField(_(u'Meta title'), blank=True, null=True, default='')
    seo_keywords = models.TextField(_(u'Meta keywords'), blank=True, null=True, default='')
    seo_description = models.TextField(_(u'Meta description'), blank=True, null=True, default='')

    discount = models.PositiveIntegerField(blank=True, default=0, null=True)
    discount_percent = models.PositiveIntegerField(choices=DISCOUNT_CHOICES, blank=True, default=1, null=True)
    discount_start_date = models.DateTimeField(blank=True, null=True)
    discount_end_date = models.DateTimeField(blank=True, null=True)

    related_products = models.ManyToManyField('self', verbose_name=u'Сопутствующие товары', blank=True)

    user = models.ForeignKey(User, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PublishedManager()

    image_types = {
        'media': (620, 400),
        'detail': (800, 400),
    }

    class Meta:
        verbose_name = _(u'Товар')
        verbose_name_plural = _(u'Товары')

    def __unicode__(self):
        return self.title

    @property
    def tags(self):
        tags = u', '.join((self.title, self.slug))
        if self.user:
            if self.user.profile:
                tags += u', ' + self.user.profile.company_name
        if self.brand:
            tags += u', '+self.brand
        if self.collection:
            tags += u', '+self.collection
        return tags + u', ' + self.category.tags

    @property
    def total(self):
        if self.discount and self.price:
            if self.discount_start_date and self.discount_end_date:
                if timezone.now() > self.discount_end_date and timezone.now() < self.discount_start_date:
                    return self.price
                if self.discount_percent == 1:
                    return int(self.price - self.price/100 * self.discount)
                else:
                    return int(self.price - self.discount)

        return self.price if self.price else 0

    @property
    def grant_total(self):
        if self.discount:
            if self.discount_percent == 1:
                return int(self.price - self.price / 100 * self.discount)
            else:
                return int(self.price - self.discount)
        return self.price

    @property
    def desc(self):
        return self.description if self.description else self.brief

    @models.permalink
    def get_absolute_url(self):
        return ('product_detail', [self.category.pk, self.category.slug,
                                   self.pk, self.slug])

    @property
    def url(self):
        return self.get_absolute_url()

    @models.permalink
    def get_product_delete_url(self):
        return ('product_delete', [self.pk, self.slug])

    @property
    def url_delete(self):
        return self.get_product_delete_url()
    @models.permalink
    def get_product_update_url(self):
        return ('product_update', [self.pk, self.slug])

    @property
    def url_update(self):
        return self.get_product_update_url()

    @models.permalink
    def get_product_seo_update_url(self):
        return ('product_seo_update', [self.pk, self.slug])

    @property
    def url_seo_update(self):
        return self.get_product_seo_update_url()

    @models.permalink
    def get_product_discount_update_url(self):
        return ('product_discount_update', [self.pk, self.slug])

    @property
    def url_discount_update(self):
        return self.get_product_discount_update_url()

    @models.permalink
    def get_characteristic_create_url(self):
        return ('product_characteristic_create', [self.pk, self.slug])

    @property
    def characteristic_create_url(self):
        return self.get_characteristic_create_url()

    @models.permalink
    def get_review_create_url(self):
        return ('review_create', [self.pk, self.slug])

    @property
    def review_create_url(self):
        return self.get_review_create_url()

    @cached_property
    def image(self):
        return self.productimage_set.first()

    @cached_property
    def images(self):
        if self.productimage_set.count():
            return self.productimage_set.all()
        else:
            return []

    @cached_property
    def similar_products(self):
        return self.category.product_set.exclude(id=self.id)[:12]

    @cached_property
    def similar_shops(self):
        ids = self.category.product_set.exclude(id=self.id, user__isnull=True).\
            values_list('user__id', flat=True).order_by('?')
        ids = list(set(ids))[:12]
        if not ids:
            ids = Product.objects.published().exclude(id=self.id, user__isnull=True). \
                values_list('user__id', flat=True).order_by('?')
            ids = list(set(ids))[:12]
        return User.objects.filter(id__in=ids)

    @property
    def reviews(self):
        return self.review_set.filter(active=True)[:20]

    @property
    def previous_product(self):
        return self.previous_next_products[0]

    @property
    def next_product(self):
        return self.previous_next_products[1]

    @property
    def previous_next_products(self):
        previous_next = getattr(self, 'previous_next', None)

        if previous_next is None:
            if not self.active:
                previous_next = (None, None)
                setattr(self, 'previous_next', previous_next)
                return previous_next

            products = list(self.__class__.objects.published())
            index = products.index(self)
            try:
                previous = products[index + 1]
            except IndexError:
                previous = products[-1]

            if index:
                _next = products[index - 1]
            else:
                _next = products[0]
            previous_next = (previous, _next)
            setattr(self, 'previous_next', previous_next)
        return previous_next


class ProductImage(ImageModelMixin, models.Model):
    """Model for product images"""
    product = models.ForeignKey(Product)
    file = models.ImageField(
        upload_to=upload_to_dir_product)

    image_types = {
        'media': (620, 400),
        'detail': (800, 400),
    }

    def delete(self, using=None):
        super(ProductImage, self).delete(using)
        self.file.delete(save=False)

    delete.alters_data = True


class ProductCharacteristic(models.Model):
    active = models.BooleanField(_('Active'), default=True)
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    title = models.CharField(_(u'Название характеристики'), max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, max_length=255)
    characteristic_desc = models.TextField(_(u'Описание'), blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = PublishedManager()

    class Meta:
        verbose_name = _(u'Характеристика товара')
        verbose_name_plural = _(u'Характеристики товара')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('product_characteristic_create', [self.product.pk, self.product.slug])

    @property
    def url(self):
        return self.get_absolute_url()

    @models.permalink
    def get_delete_url(self):
        return ('product_characteristic_delete', [self.product.pk, self.product.slug, self.pk])

    @property
    def url_delete(self):
        return self.get_delete_url()


class Review(models.Model):
    active = models.BooleanField(_('Active'), default=False)
    product = models.ForeignKey(Product, verbose_name=u'Товар')
    title = models.CharField(_(u'Ваше имя'), max_length=200)
    rating = models.PositiveIntegerField(u'Рейтинг')
    message = models.TextField(u'Ваш отзыв')

    user = models.ForeignKey(User, blank=True, null=True)
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