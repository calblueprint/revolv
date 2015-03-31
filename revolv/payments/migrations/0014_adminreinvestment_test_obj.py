# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0013_auto_20150315_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminreinvestment',
            name='test_obj',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
