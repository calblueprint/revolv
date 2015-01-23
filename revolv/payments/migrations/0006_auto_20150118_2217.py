# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_delete_paymentmanager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='entrant',
            field=models.ForeignKey(related_name=b'entrant', to='base.RevolvUserProfile'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(to='base.RevolvUserProfile', null=True),
        ),
    ]
