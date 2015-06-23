# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0012_auto_20150623_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='project_count_statistic_bottom_description_text',
            field=models.CharField(default=b'', help_text=b"The bottom section of the description of the project count statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
