# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0053_auto_20150722_0413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.CharField(default=b'DR', max_length=2, choices=[(b'AC', b'Active'), (b'ST', b'Staged'), (b'PR', b'Proposed'), (b'CO', b'Completed'), (b'DR', b'Drafted')]),
            preserve_default=True,
        ),
    ]
