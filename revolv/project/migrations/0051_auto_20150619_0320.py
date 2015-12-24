# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0050_auto_20150615_0435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='yearlyescalatorrate',
            name='project',
        ),
        migrations.DeleteModel(
            name='YearlyEscalatorRate',
        ),
    ]
