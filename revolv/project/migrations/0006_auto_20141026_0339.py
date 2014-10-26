# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20141026_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(),
        ),
    ]
