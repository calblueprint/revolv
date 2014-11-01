# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_remove_project_cover_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='cover_photo',
            field=imagekit.models.fields.ProcessedImageField(default=None, upload_to=b'covers'),
            preserve_default=True,
        ),
    ]
