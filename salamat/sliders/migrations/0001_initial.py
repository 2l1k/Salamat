# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('image', models.ImageField(upload_to=b'slider/images', verbose_name='Image')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='position')),
                ('place', models.PositiveIntegerField(default=1, verbose_name='\u041f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', choices=[(1, '\u0413\u043b\u0430\u0432\u043d\u0430\u044f \u0441\u0442\u0440 \u0442\u043e\u043f')])),
                ('link', models.URLField(max_length=255, null=True, verbose_name='link', blank=True)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True, verbose_name='banner published')),
                ('clicks', models.IntegerField(default=0)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('position', 'id'),
                'verbose_name': '\u0421\u043b\u0430\u0439\u0434\u0435\u0440',
                'verbose_name_plural': '\u0421\u0434\u0430\u0439\u0434\u0435\u0440\u044b',
            },
        ),
    ]
