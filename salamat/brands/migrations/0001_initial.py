# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('icon', models.ImageField(upload_to=b'brand/images')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='position')),
                ('link', models.URLField(max_length=255, null=True, verbose_name='link', blank=True)),
                ('active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('position', 'id'),
                'verbose_name': '\u0411\u0440\u0435\u043d\u0434',
                'verbose_name_plural': '\u0411\u0440\u0435\u043d\u0434\u044b',
            },
        ),
    ]
