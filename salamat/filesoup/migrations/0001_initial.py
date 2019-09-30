# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-12-20 11:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import filesoup.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlotFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=255, upload_to=filesoup.helpers.upload_to_dir_slot_file)),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('folder', models.CharField(db_index=True, max_length=255)),
            ],
            options={
                'ordering': ('date',),
                'abstract': False,
            },
        ),
    ]
