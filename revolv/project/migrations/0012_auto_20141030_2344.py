# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_auto_20141030_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cover_photo',
            field=imagekit.models.fields.ProcessedImageField(default=None, help_text=b'Choose a beautiful high resolution image to represent this project.', upload_to=b'covers'),
        ),
        migrations.AlterField(
            model_name='project',
            name='org_name',
            field=models.CharField(help_text=b'What is the name of the organizatoin being helped?', max_length=255, verbose_name=b'Organization Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='video_url',
            field=models.URLField(help_text=b'Optional: Link to a Youtube video about the project or community.', max_length=255, verbose_name=b'Video URL', blank=True),
        ),
    ]
