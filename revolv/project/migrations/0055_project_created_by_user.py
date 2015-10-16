# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_revolvuserprofile_preferred_categories'),
        ('project', '0054_auto_20150722_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_by_user',
            field=models.ForeignKey(related_name='created_by_user', default=1, to='base.RevolvUserProfile'),
            preserve_default=False,
        ),
    ]
