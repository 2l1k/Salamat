# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filesoup.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='logo',
            field=models.ImageField(default='sdsd', upload_to=filesoup.helpers.upload_to_dir_projects, verbose_name='Logo'),
            preserve_default=False,
        ),
    ]
