# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(verbose_name='Active')),
                ('category', models.SmallIntegerField(choices=[(1, '\u0422\u043e\u0440\u0433\u043e\u0432\u044b\u0435 \u043f\u043b\u043e\u0449\u0430\u0434\u0438'), (2, '\u0421\u0434\u0430\u044e\u0442\u0441\u044f \u0432 \u0430\u0440\u0435\u043d\u0434\u0443')])),
                ('area', models.SmallIntegerField(default=0, help_text='\u043a\u0432.\u043c', verbose_name='\u041f\u043b\u043e\u0449\u0430\u0434\u044c')),
                ('building', models.SmallIntegerField(verbose_name='\u0417\u0434\u0430\u043d\u0438\u0435', choices=[(1, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-1'), (2, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-2'), (3, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-3'), (4, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-4'), (5, '\u0421\u0430\u043b\u0430\u043c\u0430\u0442-5')])),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
