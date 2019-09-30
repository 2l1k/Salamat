# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0009_auto_20180913_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('title', models.CharField(max_length=200, verbose_name='\u0412\u0430\u0448\u0435 \u0438\u043c\u044f')),
                ('rating', models.PositiveIntegerField(verbose_name='\u0420\u0435\u0439\u0442\u0438\u043d\u0433')),
                ('message', models.TextField(verbose_name='\u0412\u0430\u0448 \u043e\u0442\u0437\u044b\u0432')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(verbose_name='\u0422\u043e\u0432\u0430\u0440', to='catalog.Product')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u041e\u0442\u0437\u044b\u0432',
                'verbose_name_plural': '\u041e\u0442\u0437\u044b\u0432\u044b',
            },
        ),
    ]
