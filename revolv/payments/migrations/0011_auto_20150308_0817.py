# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0030_remove_project_repayments'),
        ('base', '0004_revolvuserprofile_repayments'),
        ('payments', '0010_adminrepayment_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminreinvestment',
            name='admin',
            field=models.ForeignKey(default=0, to='base.RevolvUserProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminreinvestment',
            name='amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminreinvestment',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2015, 3, 8), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adminreinvestment',
            name='project',
            field=models.ForeignKey(default=0, to='project.Project'),
            preserve_default=False,
        ),
    ]
