# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0028_sharethissettings_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharethissettings',
            name='description',
            field=models.CharField(help_text=b'The description that will be used in ShareThis widget', max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sharethissettings',
            name='image',
            field=models.URLField(help_text=b'The Url of image that will be used in ShareThis widget', verbose_name=b'Image Url'),
            preserve_default=True,
        ),
    ]
