# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_newsletteruser'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletteruser',
            name='subscribed_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 31, 22, 42, 16, 425), auto_now_add=True),
            preserve_default=True,
        ),
    ]
