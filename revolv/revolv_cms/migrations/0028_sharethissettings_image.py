# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0027_remove_sharethissettings_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharethissettings',
            name='image',
            field=models.ImageField(default=b'd.png', help_text=b'ShareThis Image', upload_to=b'images'),
            preserve_default=True,
        ),
    ]
