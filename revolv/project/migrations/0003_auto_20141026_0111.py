# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='actual_energy',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='project',
            name='amount_repaid',
            field=models.DecimalField(default=0.0, max_digits=15, decimal_places=2),
        ),
    ]
