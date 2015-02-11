# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_auto_20150119_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(to='base.RevolvUserProfile'),
        ),
    ]
