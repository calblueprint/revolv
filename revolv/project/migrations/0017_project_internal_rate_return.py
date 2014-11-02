# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_auto_20141101_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='internal_rate_return',
            field=models.DecimalField(default=0.0, help_text=b'The internal rate of return for this project.', verbose_name=b'Internal Rate of Return', max_digits=6, decimal_places=3),
            preserve_default=True,
        ),
    ]
