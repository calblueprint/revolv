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
            name='solar_data',
            field=models.FileField(upload_to=b'project<built-in function id>'),
        ),
    ]
