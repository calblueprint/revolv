# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0029_auto_20150527_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminadjustment',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 5, 29, 21, 3, 56, 116982), verbose_name=b'What time period should this transaction be recorded under?'),
        ),
    ]
