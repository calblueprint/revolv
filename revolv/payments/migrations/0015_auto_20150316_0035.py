# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_adminreinvestment_test_obj'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminreinvestment',
            name='test_obj',
        ),
        migrations.RemoveField(
            model_name='adminrepayment',
            name='linked_to_users',
        ),
    ]
