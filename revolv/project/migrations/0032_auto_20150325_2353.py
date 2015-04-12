# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0031_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cover_photo',
            field=imagekit.models.fields.ProcessedImageField(default=None, help_text=b'Choose a beautiful high resolution image to represent this project.', upload_to=b'covers/'),
        ),
    ]
