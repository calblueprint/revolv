# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0059_auto_20151031_2137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectproperty',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectProperty',
        ),
        migrations.AddField(
            model_name='project',
            name='is_paid_off',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='monthly_reinvestment_cap',
            field=models.FloatField(default=0.0, blank=True),
            preserve_default=True,
        ),
    ]
