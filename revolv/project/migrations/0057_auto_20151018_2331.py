# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0056_auto_20151011_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ambassador',
            field=models.ForeignKey(related_name='ambassador', to='base.RevolvUserProfile', null=True),
            preserve_default=True,
        ),
    ]
