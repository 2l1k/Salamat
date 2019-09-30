# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_auto_20180904_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='apartment',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='building',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='\u0417\u0434\u0430\u043d\u0438\u0435', choices=[(1, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-1'), (2, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-2'), (3, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-3'), (4, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-4'), (5, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-5')]),
        ),
        migrations.AddField(
            model_name='customer',
            name='floor',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='company_name',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contract_number',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
