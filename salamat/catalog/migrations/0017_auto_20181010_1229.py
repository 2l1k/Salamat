# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20180921_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.CharField(default=b'', max_length=200, null=True, verbose_name='\u0411\u0440\u0435\u043d\u0434', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='collection',
            field=models.CharField(default=b'', max_length=200, null=True, verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(default=b'', max_length=200, null=True, verbose_name='\u0426\u0432\u0435\u0442', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(default=b'', null=True, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_description',
            field=models.TextField(default=b'', null=True, verbose_name='Meta description', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_keywords',
            field=models.TextField(default=b'', null=True, verbose_name='Meta keywords', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='seo_title',
            field=models.TextField(default=b'', null=True, verbose_name='Meta title', blank=True),
        ),
    ]
