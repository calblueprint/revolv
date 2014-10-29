# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_auto_20141029_0410'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='cover_photo',
        ),
    ]
