# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0046_auto_20150504_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(help_text=b'This is the body of text that shows up on the project page.', verbose_name=b'Project description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='mission_statement',
            field=models.TextField(help_text=b'What is the mission statement of the organization being helped by this project?', verbose_name=b'Organization Mission'),
        ),
    ]
