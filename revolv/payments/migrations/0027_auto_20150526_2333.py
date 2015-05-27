# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0026_auto_20150526_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminadjustment',
            name='admin',
        ),
        migrations.AlterField(
            model_name='adminadjustment',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 5, 26, 23, 33, 5, 508954)),
        ),
    ]
