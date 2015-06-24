# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0017_auto_20150624_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='carbon_dioxide_statistic_bottom_description_text',
            field=models.CharField(default=b'of carbon dioxide', help_text=b"The bottom section of the description of the carbon dioxide statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='carbon_dioxide_statistic_top_description_text',
            field=models.CharField(default=b'saved', help_text=b"The top section of the description of the carbon dioxide statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='kwh_statistic_top_description_text',
            field=models.CharField(default=b'generated', help_text=b"The top section of the description of the kilowatt-hours statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='last_statistic_description_text',
            field=models.CharField(default=b'Help us save the world by going solar!', help_text=b"The description of the bottom right icon on the 'My Impact' section of the dashboard. Unlike the other statistics on this page, this last section only has one text field.", max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='project_count_statistic_top_description_text',
            field=models.CharField(default=b'contributed to', help_text=b"The top section of the description of the project count statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='repayment_statistic_bottom_description_text',
            field=models.CharField(default=b'in repayments', help_text=b"The bottom section of the description of the repayments statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='repayment_statistic_top_description_text',
            field=models.CharField(default=b'earned', help_text=b"The top section of the description of the repayments statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='trees_saved_statistic_top_description_text',
            field=models.CharField(default=b'saved', help_text=b"The top section of the description of the trees saved statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
