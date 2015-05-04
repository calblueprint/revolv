# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0044_auto_20150504_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='mission_statement',
            field=models.TextField(default='this is the mission statement!', help_text=b'What is the mission statement of the organization being helped by this project?', verbose_name=b'Organization Mission'),
            preserve_default=False,
        ),
    ]
