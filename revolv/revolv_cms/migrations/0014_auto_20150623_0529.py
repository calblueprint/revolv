# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0013_auto_20150623_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardimpactsettings',
            name='impact_statistics_header_text',
            field=models.CharField(default=b'Thank you for contributing! Your contribution has...', help_text=b"The heading above the statistics in the 'My Impact' section of the dashboard, e.g. 'Thank you for contributing! Your contribution has...'.", max_length=90),
            preserve_default=True,
        ),
    ]
