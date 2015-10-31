# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0058_projectproperty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectproperty',
            name='name',
            field=models.CharField(max_length=4),
            preserve_default=True,
        ),
    ]
