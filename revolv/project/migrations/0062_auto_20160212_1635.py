# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0061_auto_20160209_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cover_photo',
            field=imagekit.models.fields.ProcessedImageField(default=None, help_text=b'Choose a beautiful high resolution image to represent this project.', upload_to=b'covers/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='video_url',
            field=models.URLField(help_text=b'Link to a Youtube video about the project or community.', max_length=255, verbose_name=b'Video URL'),
            preserve_default=True,
        ),
    ]
