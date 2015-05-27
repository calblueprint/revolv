# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0025_auto_20150526_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminadjustment',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 5, 26, 20, 57, 25, 150907)),
        ),
    ]
