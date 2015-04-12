# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_projectupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectupdate',
            name='update_text',
            field=models.TextField(help_text=b'What should the update say?', verbose_name=b'Update text'),
        ),
    ]
