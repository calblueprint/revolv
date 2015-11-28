# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0026_sharethissettings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sharethissettings',
            name='image',
        ),
    ]
