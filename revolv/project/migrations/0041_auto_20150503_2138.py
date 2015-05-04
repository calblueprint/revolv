# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0040_auto_20150503_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationlevel',
            name='amount',
            field=models.IntegerField(default=b'0'),
        ),
        migrations.AlterField(
            model_name='donationlevel',
            name='description',
            field=models.TextField(default=b'A donation level!'),
        ),
    ]
