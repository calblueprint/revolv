# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_auto_20150308_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminrepayment',
            name='linked_to_users',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='payment',
            name='adminreinvestment',
            field=models.ForeignKey(blank=True, to='payments.AdminReinvestment', null=True),
            preserve_default=True,
        ),
    ]
