# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0025_project_solar_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='annual_solar_data',
            field=models.FileField(null=True, upload_to=b'projects/annual/'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='daily_solar_data',
            field=models.FileField(null=True, upload_to=b'projects/daily/'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='monthly_solar_data',
            field=models.FileField(null=True, upload_to=b'projects/monthly/'),
            preserve_default=True,
        ),
    ]
