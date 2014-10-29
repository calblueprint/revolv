# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_auto_20141029_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='cover_photo',
            field=imagekit.models.fields.ProcessedImageField(upload_to=b'covers'),
        ),
    ]
