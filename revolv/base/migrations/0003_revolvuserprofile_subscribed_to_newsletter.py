# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20141102_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='revolvuserprofile',
            name='subscribed_to_newsletter',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
