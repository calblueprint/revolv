# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_auto_20141030_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='funding_goal',
            field=models.DecimalField(help_text=b'How much do you aim to raise for this project?', max_digits=15, decimal_places=2),
        ),
    ]
