# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_auto_20141106_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ambassador',
            field=models.ForeignKey(related_name=b'ambassador', to='base.RevolvUserProfile'),
        ),
    ]
