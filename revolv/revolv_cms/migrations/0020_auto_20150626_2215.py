# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0019_auto_20150625_0447'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='donor_stats_table_days_so_far_description',
            field=models.CharField(default=b'Days so far', help_text=b"The description to be displayed next to the 'days so far' statistic in the dashboard project statistics area. e.g. 'Days so far' or 'Days since start'", max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='donor_stats_table_donors_description',
            field=models.CharField(default=b'Donors', help_text=b"The description to be displayed next to the number of donors statistic in the dashboard project statistics area. e.g. 'Donors' or 'Total Donors'", max_length=30),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='donor_stats_table_timeline_description',
            field=models.CharField(default=b'Timeline', help_text=b"The description to be displayed next to the project timeline (total number of days for the campaign) statistic in the dashboard project statistics area. e.g. 'Timeline'", max_length=30),
            preserve_default=True,
        ),
    ]
