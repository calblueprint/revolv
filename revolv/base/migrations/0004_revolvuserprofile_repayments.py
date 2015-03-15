# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_auto_20150308_0313'),
        ('base', '0003_revolvuserprofile_subscribed_to_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='revolvuserprofile',
            name='repayments',
            field=models.ManyToManyField(to='payments.AdminRepayment'),
            preserve_default=True,
        ),
    ]
