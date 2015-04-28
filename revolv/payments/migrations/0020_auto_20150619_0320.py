# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0019_auto_20150615_0435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminrepayment',
            name='admin',
            field=models.ForeignKey(blank=True, to='base.RevolvUserProfile', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adminrepayment',
            name='organizational_cost',
            field=models.DecimalField(max_digits=8, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adminrepayment',
            name='reinvestable',
            field=models.DecimalField(max_digits=8, decimal_places=3),
            preserve_default=True,
        ),
    ]
