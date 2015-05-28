# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0028_auto_20150527_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminadjustment',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 5, 27, 19, 34, 26, 325563), verbose_name=b'What time period should this transaction be recorded under?'),
        ),
    ]
