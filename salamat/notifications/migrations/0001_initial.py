# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('position', models.PositiveIntegerField(default=0, verbose_name='position')),
                ('link', models.URLField(max_length=255, null=True, verbose_name='link', blank=True)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('position', 'id'),
                'verbose_name': '\u0423\u0432\u0435\u0434\u043e\u043b\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0423\u0432\u0435\u0434\u043e\u043b\u0435\u043d\u0438\u044f',
            },
        ),
    ]
