# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0041_auto_20150503_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationlevel',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='donationlevel',
            name='description',
            field=models.TextField(default=b''),
        ),
    ]
