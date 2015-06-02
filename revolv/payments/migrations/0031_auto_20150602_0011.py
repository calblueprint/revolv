# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0030_auto_20150529_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminadjustment',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 6, 2, 0, 11, 30, 650586), verbose_name=b'What time period should this transaction be recorded under?'),
        ),
    ]
