# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0017_project_internal_rate_return'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='ambassador',
            field=models.ForeignKey(default='1', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='project_status',
            field=models.CharField(default=b'DR', max_length=2, choices=[(b'AC', b'Accepted'), (b'PR', b'Proposed'), (b'CO', b'Completed'), (b'DR', b'Drafted')]),
        ),
    ]
