# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0018_auto_20141103_1913'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='donors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='ambassador',
            field=models.ForeignKey(related_name=b'ambassador', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
