# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0005_customer_whatsapp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='company_desc',
            field=models.TextField(null=True, blank=True),
        ),
    ]
