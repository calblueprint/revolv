# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0020_auto_20150626_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectstatisticssettings',
            name='people_affected_description',
            field=models.CharField(default=b'Number of people affected', help_text=b"The description to be displayed next to the 'people affected' statistic in the dashboard project statistics area. e.g. 'Number of people affected' or 'People affected'", max_length=30),
            preserve_default=True,
        ),
    ]
