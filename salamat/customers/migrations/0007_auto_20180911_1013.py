# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_customer_company_desc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='company_desc',
            field=models.TextField(default=b'', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='whatsapp',
            field=models.CharField(default=b'', max_length=30, null=True, verbose_name='Whatsapp', blank=True),
        ),
    ]
