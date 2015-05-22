# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0023_auto_20150520_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminadjustment',
            name='cash_type',
            field=models.CharField(default='cash_in', max_length=10, choices=[(b'cash_in', b'Cash in'), (b'cash_out', b'Cash out')]),
            preserve_default=False,
        ),
    ]
