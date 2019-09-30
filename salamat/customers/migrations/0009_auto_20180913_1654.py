# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0008_auto_20180913_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='building',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='\u0417\u0434\u0430\u043d\u0438\u0435', choices=[(1, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442 1'), (2, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442 2'), (3, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442 3'), (4, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442 4'), (5, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442 5')]),
        ),
    ]
