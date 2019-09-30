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
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='Title')),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'title', unique=True, max_length=255, editable=False)),
                ('active', models.BooleanField(verbose_name='Active')),
                ('image', models.ImageField(upload_to=filesoup.helpers.upload_to_dir_projects, verbose_name='Preview')),
                ('description', models.TextField(null=True, verbose_name='Description', blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=(baseapp.mixins.ImageURLProvidingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.ImageField(upload_to=filesoup.helpers.upload_to_dir_projects)),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
            bases=(baseapp.mixins.ImageModelMixin, models.Model),
        ),
    ]
