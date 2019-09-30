# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20180917_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='in_stock',
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=1, verbose_name='\u0412 \u043d\u0430\u043b\u0438\u0447\u0438\u0438', choices=[(1, '\u0412 \u043d\u0430\u043b\u0438\u0447\u0438\u0438'), (2, '\u041d\u0435\u0442 \u0432 \u043d\u0430\u043b\u0438\u0447\u0438\u0438'), (3, '\u041f\u043e\u0434 \u0437\u0430\u043a\u0430\u0437'), (4, '\u041e\u0436\u0438\u0434\u0430\u0435\u0442\u0441\u044f')]),
        ),
    ]
