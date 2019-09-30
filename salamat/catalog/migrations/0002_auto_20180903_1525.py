# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': '\u0422\u043e\u0432\u0430\u0440', 'verbose_name_plural': '\u0422\u043e\u0432\u0430\u0440\u044b'},
        ),
        migrations.AlterModelOptions(
            name='productcategory',
            options={'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', 'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438'},
        ),
        migrations.AlterModelOptions(
            name='productcharacteristic',
            options={'verbose_name': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0430 \u0442\u043e\u0432\u0430\u0440\u0430', 'verbose_name_plural': '\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440\u0438\u0441\u0442\u0438\u043a\u0438 \u0442\u043e\u0432\u0430\u0440\u0430'},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'verbose_name': '\u0422\u0438\u043f \u0442\u043e\u0432\u0430\u0440\u0430', 'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0442\u043e\u0432\u0430\u0440\u0430'},
        ),
        migrations.AddField(
            model_name='productcategory',
            name='icon',
            field=models.ImageField(default='', upload_to=b'catalog/category/icons', verbose_name='Icon'),
            preserve_default=False,
        ),
    ]
