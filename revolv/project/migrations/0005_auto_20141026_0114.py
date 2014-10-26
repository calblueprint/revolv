# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20141026_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='org_about',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='project',
            name='org_name',
            field=models.CharField(max_length=255),
        ),
    ]
