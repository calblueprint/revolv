# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0039_auto_20150428_0246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yearlyescalatorrate',
            old_name='amount',
            new_name='rate',
        ),
    ]
