# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0021_auto_20150519_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminadjustment',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
