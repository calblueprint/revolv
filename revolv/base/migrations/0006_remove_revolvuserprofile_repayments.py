# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_revolvuserprofile_reinvest_pool'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revolvuserprofile',
            name='repayments',
        ),
    ]
