# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0037_auto_20150414_0117'),
        ('base', '0006_remove_revolvuserprofile_repayments'),
    ]

    operations = [
        migrations.AddField(
            model_name='revolvuserprofile',
            name='preferred_categories',
            field=models.ManyToManyField(to='project.Category'),
            preserve_default=True,
        ),
    ]
