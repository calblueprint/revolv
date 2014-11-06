# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20141102_0206'),
        ('project', '0018_auto_20141103_1913'),
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
            field=models.ForeignKey(related_name=b'ambassador', to=settings.AUTH_USER_MODEL),
        ),
    ]
