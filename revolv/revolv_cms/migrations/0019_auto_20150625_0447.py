# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0018_auto_20150624_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='repayment_statistic_bottom_description_text',
            field=models.CharField(default=b'to reinvest', help_text=b"The bottom section of the description of the repayments statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='trees_saved_statistic_bottom_description_text',
            field=models.CharField(default=b'of trees', help_text=b"The bottom section of the description of the trees saved statistic on the 'My Impact' section of the dashboard. There are three sections to every statistic description. The top section is the first line, the middle section is the actual statistic (which is calculated and not editable) and is shown bold and in color, and the bottom section is the last line.", max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
