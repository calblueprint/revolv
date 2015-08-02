# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0022_auto_20150722_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='repayment_stats_table_amount_donated_description',
            field=models.CharField(default=b'Amount Donated', help_text=b'The description to be displayed next to the amount donated statistic in the dashboard project repayment statistics area.', max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='repayment_stats_table_amount_repaid_description',
            field=models.CharField(default=b'Amount Repaid', help_text=b'The description to be displayed next to the amount repaid statistic in the dashboard project repayment statistics area.', max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='repayment_stats_table_kwh_saved_description',
            field=models.CharField(default=b'Amount Remaining', help_text=b'The description to be displayed next to the kwh saved statistic in the dashboard project repayment statistics area.', max_length=30),
            preserve_default=True,
        ),
    ]
