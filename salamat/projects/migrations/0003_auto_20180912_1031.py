# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filesoup.helpers


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.ImageField(upload_to=filesoup.helpers.upload_to_dir_projects, null=True, verbose_name='Logo', blank=True),
        ),
    ]
