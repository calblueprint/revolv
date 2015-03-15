# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_revolvuserprofile_repayments'),
        ('project', '0032_remove_project_donors'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='donors',
            field=models.ManyToManyField(to='base.RevolvUserProfile'),
            preserve_default=True,
        ),
    ]
