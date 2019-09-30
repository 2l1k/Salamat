# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20180919_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.PositiveIntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_percent',
            field=models.PositiveIntegerField(default=1, null=True, blank=True, choices=[(1, '%'), (2, '\u0442\u0433')]),
        ),
    ]
