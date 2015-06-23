# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0049_auto_20150615_0053'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
