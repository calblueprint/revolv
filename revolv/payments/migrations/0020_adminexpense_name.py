# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0019_adminexpense'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminexpense',
            name='name',
            field=models.CharField(default='generic name', max_length=100),
            preserve_default=False,
        ),
    ]
