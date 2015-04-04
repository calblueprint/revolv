# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0017_manual_reinvestmentfragment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, to='base.RevolvUserProfile', null=True),
        ),
    ]
