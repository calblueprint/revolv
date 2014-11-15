# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20141102_0206'),
        ('project', '0023_auto_20141108_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='donors',
            field=models.ManyToManyField(to='base.RevolvUserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='ambassador',
            field=models.ForeignKey(related_name=b'ambassador', to='base.RevolvUserProfile'),
        ),
    ]
