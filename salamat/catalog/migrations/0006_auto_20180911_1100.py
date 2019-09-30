# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20180903_1604'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='icon_red',
            field=models.ImageField(upload_to=b'catalog/category/icons', null=True, verbose_name='Icon red', blank=True),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='icon',
            field=models.ImageField(upload_to=b'catalog/category/icons', null=True, verbose_name='Icon white', blank=True),
        ),
    ]
