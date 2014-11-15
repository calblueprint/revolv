# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0022_remove_project_donors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ambassador',
            field=models.ForeignKey(to='base.RevolvUserProfile'),
        ),
    ]
