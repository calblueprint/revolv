# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0010_project_cover_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='mission_statement',
            field=models.TextField(help_text=b'What is the mission statement of the organization being helped by this project?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='org_about',
            field=models.TextField(help_text=b'Elaborate more about the organization, what it does, who it serves, etc.', verbose_name=b'Organization Description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='org_name',
            field=models.CharField(max_length=255, verbose_name=b'Organization Description'),
        ),
    ]
