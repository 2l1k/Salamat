# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20180912_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='seo_keywords',
            field=models.TextField(null=True, verbose_name='Meta keywords', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_title',
            field=models.TextField(null=True, verbose_name='Meta title', blank=True),
        ),
    ]
