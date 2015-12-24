# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0018_auto_20150320_0712'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminrepayment',
            name='amount',
        ),
        migrations.AddField(
            model_name='adminrepayment',
            name='organizational_cost',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminrepayment',
            name='reinvestable',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
