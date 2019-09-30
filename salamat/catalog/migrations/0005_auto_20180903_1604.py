# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20180903_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0411\u0440\u0435\u043d\u0434', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.CharField(max_length=200, null=True, verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0426\u0432\u0435\u0442', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(null=True, verbose_name='\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430', blank=True),
        ),
    ]
