# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0038_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='mission_statement',
        ),
        migrations.AddField(
            model_name='project',
            name='description',
            field=models.TextField(default='This is the description of the project!', help_text=b'Elaborate more about the project, the goals, etc.', verbose_name=b'Project description'),
            preserve_default=False,
        ),
    ]
