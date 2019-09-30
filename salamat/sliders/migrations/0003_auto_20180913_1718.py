# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sliders', '0002_auto_20180911_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slider',
            name='place',
            field=models.PositiveIntegerField(default=1, verbose_name='\u041f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', choices=[(1, '\u0413\u043b\u0430\u0432\u043d\u0430\u044f \u0441\u0442\u0440 \u0442\u043e\u043f'), (2, '\u0413\u0430\u043b\u0435\u0440\u0435\u044f')]),
        ),
    ]
