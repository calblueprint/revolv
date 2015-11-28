# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_revolvuserprofile_preferred_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='revolvuserprofile',
            name='subscribed_to_updates',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
