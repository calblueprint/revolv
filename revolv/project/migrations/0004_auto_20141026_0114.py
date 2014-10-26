# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20141026_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='location_latitude',
            field=models.DecimalField(default=0.0, max_digits=17, decimal_places=14),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='location_longitude',
            field=models.DecimalField(default=0.0, max_digits=17, decimal_places=14),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='org_about',
            field=models.CharField(default=b'Re-volv Partner', max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='org_name',
            field=models.CharField(default=b'Re-volv Partner', max_length=255),
            preserve_default=True,
        ),
    ]
