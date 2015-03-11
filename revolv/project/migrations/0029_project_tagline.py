# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0028_remove_project_amount_repaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tagline',
            field=models.CharField(help_text=b'Select a short tag line that describes this project. (No more than 100 characters.)', max_length=100, null=True),
            preserve_default=True,
        ),
    ]
