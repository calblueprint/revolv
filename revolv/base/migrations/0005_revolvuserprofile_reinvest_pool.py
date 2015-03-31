# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_revolvuserprofile_repayments'),
    ]

    operations = [
        migrations.AddField(
            model_name='revolvuserprofile',
            name='reinvest_pool',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
