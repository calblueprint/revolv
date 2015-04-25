# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donationlevel',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='projectupdate',
            name='project',
            field=models.ForeignKey(related_name=b'updates', to='project.Project'),
        ),
    ]
