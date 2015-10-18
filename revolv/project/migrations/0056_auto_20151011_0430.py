# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0055_project_created_by_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ambassador',
            field=models.ForeignKey(related_name='ambassador', to='base.RevolvUserProfile', null=True, default=None),
            preserve_default=True,
        ),
    ]
