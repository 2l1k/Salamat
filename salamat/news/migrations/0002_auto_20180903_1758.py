# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='brief_en',
        ),
        migrations.RemoveField(
            model_name='news',
            name='brief_ru',
        ),
        migrations.RemoveField(
            model_name='news',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='news',
            name='description_ru',
        ),
        migrations.RemoveField(
            model_name='news',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='news',
            name='title_ru',
        ),
    ]
