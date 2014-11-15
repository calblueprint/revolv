# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0019_auto_20141105_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.CharField(default=b'DR', max_length=2, choices=[(b'AC', b'Active'), (b'PR', b'Proposed'), (b'CO', b'Completed'), (b'DR', b'Drafted')]),
        ),
    ]
