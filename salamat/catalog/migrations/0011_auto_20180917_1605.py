# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-date_added',), 'verbose_name': '\u041e\u0442\u0437\u044b\u0432', 'verbose_name_plural': '\u041e\u0442\u0437\u044b\u0432\u044b'},
        ),
    ]
