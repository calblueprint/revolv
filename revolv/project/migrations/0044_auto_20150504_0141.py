# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0043_auto_20150504_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='annual_solar_data',
            field=models.FileField(null=True, upload_to=b'projects/annual/', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='cover_photo',
            field=imagekit.models.fields.ProcessedImageField(default=None, help_text=b'Choose a beautiful high resolution image to represent this project.', upload_to=b'covers/', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='daily_solar_data',
            field=models.FileField(null=True, upload_to=b'projects/daily/', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='donors',
            field=models.ManyToManyField(to=b'base.RevolvUserProfile', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='monthly_solar_data',
            field=models.FileField(null=True, upload_to=b'projects/monthly/', blank=True),
        ),
    ]
