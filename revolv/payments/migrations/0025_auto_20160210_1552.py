# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0024_auto_20160209_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tip',
            name='user',
            field=models.ForeignKey(to='base.RevolvUserProfile'),
            preserve_default=True,
        ),
    ]
