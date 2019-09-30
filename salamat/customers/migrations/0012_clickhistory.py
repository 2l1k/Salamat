# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customers', '0011_auto_20180917_1757'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClickHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.PositiveIntegerField(default=1, choices=[(1, b'Phone')])),
                ('ip', models.GenericIPAddressField(null=True, blank=True)),
                ('user_agent', models.TextField(blank=True, null=True, validators=[django.core.validators.MaxLengthValidator(1000)])),
                ('referrer', models.URLField(null=True, blank=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(related_name='clicks', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('customer', models.ForeignKey(related_name='histories', verbose_name='\u041c\u0430\u0433\u0430\u0437\u0438\u043d', to='customers.Customer')),
            ],
            options={
                'ordering': ('-date_added',),
                'verbose_name': '\u041f\u043e\u043a\u0430\u0437 \u043d\u043e\u043c\u0435\u0440\u0430',
                'verbose_name_plural': '\u041f\u043e\u043a\u0430\u0437\u044b \u043d\u043e\u043c\u0435\u0440\u043e\u0432',
            },
        ),
    ]
