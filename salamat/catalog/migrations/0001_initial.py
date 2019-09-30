# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import baseapp.mixins
from django.conf import settings
import filesoup.helpers


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, max_length=255, editable=False)),
                ('description', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430', blank=True)),
                ('price_from', models.BooleanField(default=False, verbose_name='\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c \u0446\u0435\u043d\u0443 \u043e\u0442')),
                ('price', models.FloatField(null=True, verbose_name='\u0426\u0435\u043d\u0430', blank=True)),
                ('quantity', models.IntegerField(null=True, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e', blank=True)),
                ('in_stock', models.BooleanField(default=True, verbose_name='\u0412 \u043d\u0430\u043b\u0438\u0447\u0438\u0438')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('featured', models.BooleanField(default=False, verbose_name='Featured')),
                ('seo_title', models.CharField(max_length=200, null=True, verbose_name='Meta title', blank=True)),
                ('seo_keywords', models.CharField(max_length=200, null=True, verbose_name='Meta keywords', blank=True)),
                ('seo_description', models.TextField(null=True, verbose_name='Meta description', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=(baseapp.mixins.ImageURLProvidingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, max_length=255, editable=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(related_name='childs', blank=True, to='catalog.ProductCategory', null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='ProductCharacteristic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('title', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0445\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, max_length=255, editable=False)),
                ('characteristic_desc', models.TextField(null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(verbose_name='\u0422\u043e\u0432\u0430\u0440', to='catalog.Product')),
            ],
            options={
                'verbose_name': 'Product characteristic',
                'verbose_name_plural': 'Product characteristics',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=filesoup.helpers.upload_to_dir_product)),
                ('product', models.ForeignKey(to='catalog.Product')),
            ],
            bases=(baseapp.mixins.ImageModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, max_length=255, editable=False)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Product type',
                'verbose_name_plural': 'Product types',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='catalog.ProductCategory', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f', blank=True, to='catalog.ProductType', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
