# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='post_funding_updates',
        ),
        migrations.AlterField(
            model_name='projectupdate',
            name='project',
            field=models.ForeignKey(related_name=b'updates', to='project.Project'),
        ),
    ]
