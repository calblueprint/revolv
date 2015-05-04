# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0045_project_mission_statement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='mission_statement',
            field=models.TextField(default=b'This is the mission statement!', help_text=b'What is the mission statement of the organization being helped by this project?', verbose_name=b'Organization Mission'),
        ),
    ]
