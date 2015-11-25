# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_revolvuserprofile_subscribed_to_updates'),
    ]

    operations = [
        migrations.AddField(
            model_name='revolvuserprofile',
            name='address',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
