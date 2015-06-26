# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('revolv_cms', '0011_auto_20150622_0549'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardImpactSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('impact_statistics_header_text', models.CharField(default=b'Thank you for contributing! Your contribution has...', help_text=b"The heading above the statistics in the 'My Impact' section of the dashboard, e.g. 'Thank you for contributing! Your contribution has...'.", max_length=100)),
                ('repayment_statistic_top_description_text', models.CharField(default=b'earned', help_text=b"The top section of the description of the repayments statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20)),
                ('repayment_statistic_bottom_description_text', models.CharField(default=b'in repayments', help_text=b"The bottom section of the description of the repayments statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20)),
                ('project_count_statistic_top_description_text', models.CharField(default=b'contributed to', help_text=b"The top section of the description of the project count statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20)),
                ('project_count_statistic_bottom_description_text', models.CharField(default=b'', help_text=b"The bottom section of the description of the project count statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20)),
                ('last_statistic_description_text', models.CharField(default=b'Help us save the world by going solar!', help_text=b"The description of the bottom right icon on the 'My Impact' section of the dashboard. Unlike the other statistics on this page, this last section only has one text field.", max_length=100)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='dashboardsettings',
            name='impact_statistics_header_text',
        ),
        migrations.RemoveField(
            model_name='dashboardsettings',
            name='last_statistic_description_text',
        ),
        migrations.RemoveField(
            model_name='dashboardsettings',
            name='project_count_statistic_bottom_description_text',
        ),
        migrations.RemoveField(
            model_name='dashboardsettings',
            name='project_count_statistic_top_description_text',
        ),
        migrations.RemoveField(
            model_name='dashboardsettings',
            name='repayment_statistic_bottom_description_text',
        ),
        migrations.RemoveField(
            model_name='dashboardsettings',
            name='repayment_statistic_top_description_text',
        ),
    ]
