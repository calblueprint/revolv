# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0021_projectstatisticssettings_people_affected_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='donor_stats_table_amount_donated_description',
            field=models.CharField(default=b'Amount Donated', help_text=b'The description to be displayed next to the amount donated statistic in the dashboard project statistics area.', max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='donor_stats_table_amount_remaining_description',
            field=models.CharField(default=b'Amount Remaining', help_text=b'The description to be displayed next to the amount remaining statistic in the dashboard project statistics area.', max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='donor_stats_table_funding_goal_description',
            field=models.CharField(default=b'Funding Goal', help_text=b'The description to be displayed next to the funding goal statistic in the dashboard project statistics area.', max_length=30),
            preserve_default=True,
        ),
    ]
