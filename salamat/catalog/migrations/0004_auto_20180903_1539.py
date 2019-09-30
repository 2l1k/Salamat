# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20180903_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='icon',
            field=models.ImageField(upload_to=b'catalog/category/icons', null=True, verbose_name='Icon', blank=True),
        ),
    ]
