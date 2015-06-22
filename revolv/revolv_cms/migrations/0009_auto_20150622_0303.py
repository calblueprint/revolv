# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0008_dashboardsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardsettings',
            name='project_count_statistic_bottom_description_text',
            field=models.CharField(default=b'', help_text=b"The bottom section of the description of the project count statistic on the 'My Impact' section of the dashboard.", max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardsettings',
            name='project_count_statistic_top_description_text',
            field=models.CharField(default=b'contributed to', help_text=b"The top section of the description of the project count statistic on the 'My Impact' section of the dashboard.", max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardsettings',
            name='repayment_statistic_bottom_description_text',
            field=models.CharField(default=b'in repayments', help_text=b"The bottom section of the description of the repayments statistic on the 'My Impact' section of the dashboard.", max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardsettings',
            name='repayment_statistic_top_description_text',
            field=models.CharField(default=b'earned', help_text=b"The top section of the description of the repayments statistic on the 'My Impact' section of the dashboard.", max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardsettings',
            name='impact_statistics_header_text',
            field=models.CharField(default=b'Thank you for contributing! Your contribution has...', help_text=b"The heading above the statistics in the 'My Impact' section of the dashboard, e.g. 'Thank you for contributing! Your contribution has...'.", max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectpagesettings',
            name='donors_wording',
            field=models.CharField(default=b'donors', help_text=b"The wording that will be displayed after the number of donors to the project the user is viewing. For example, 'donors' or 'contributors'.", max_length=20),
            preserve_default=True,
        ),
    ]
