# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0030_remove_project_repayments'),
        ('payments', '0009_auto_20150308_0313'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminrepayment',
            name='project',
            field=models.ForeignKey(default=1, to='project.Project'),
            preserve_default=False,
        ),
    ]
