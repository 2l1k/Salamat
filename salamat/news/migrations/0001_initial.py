# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields
import baseapp.mixins
import filesoup.helpers


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('title_en', models.CharField(max_length=100, null=True, verbose_name='Title')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, max_length=255, editable=False)),
                ('image', models.ImageField(upload_to=filesoup.helpers.upload_to_dir_news, verbose_name='Preview')),
                ('active', models.BooleanField(verbose_name='Active')),
                ('brief', models.TextField(help_text='Preview text', verbose_name='Brief')),
                ('brief_ru', models.TextField(help_text='Preview text', null=True, verbose_name='Brief')),
                ('brief_en', models.TextField(help_text='Preview text', null=True, verbose_name='Brief')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('description_ru', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('description_en', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
            bases=(baseapp.mixins.ImageURLProvidingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='NewsImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=filesoup.helpers.upload_to_dir_news)),
                ('news', models.ForeignKey(to='news.News')),
            ],
            bases=(baseapp.mixins.ImageModelMixin, models.Model),
        ),
    ]
