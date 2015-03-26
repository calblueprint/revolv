# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0031_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='donors',
        ),
    ]
