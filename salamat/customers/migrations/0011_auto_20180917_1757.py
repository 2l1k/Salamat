# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0010_review'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='creator',
            field=models.ForeignKey(related_name='shop_reviews', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
