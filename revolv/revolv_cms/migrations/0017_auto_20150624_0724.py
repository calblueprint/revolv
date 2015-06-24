# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0016_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardimpactsettings',
            name='carbon_dioxide_statistic_bottom_description_text',
            field=models.CharField(default=b'of carbon dioxide', help_text=b"The bottom section of the description of the carbon dioxide statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardimpactsettings',
            name='carbon_dioxide_statistic_top_description_text',
            field=models.CharField(default=b'saved', help_text=b"The top section of the description of the carbon dioxide statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardimpactsettings',
            name='kwh_statistic_bottom_description_text',
            field=models.CharField(default=b'of electricity', help_text=b"The bottom section of the description of the kilowatt-hours saved statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardimpactsettings',
            name='kwh_statistic_top_description_text',
            field=models.CharField(default=b'generated', help_text=b"The top section of the description of the kilowatt-hours statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardimpactsettings',
            name='trees_saved_statistic_bottom_description_text',
            field=models.CharField(default=b'', help_text=b"The bottom section of the description of the trees saved statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardimpactsettings',
            name='trees_saved_statistic_top_description_text',
            field=models.CharField(default=b'saved', help_text=b"The top section of the description of the trees saved statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20),
            preserve_default=True,
        ),
    ]
