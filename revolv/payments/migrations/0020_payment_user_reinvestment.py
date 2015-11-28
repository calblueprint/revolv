# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0019_projectmontlyrepaymentconfig_projectmontlyrepaymentconfigmanager_userreinvestment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user_reinvestment',
            field=models.ForeignKey(blank=True, to='payments.UserReinvestment', null=True),
            preserve_default=True,
        ),
    ]
