# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_auto_20150308_0313'),
        ('project', '0028_remove_project_amount_repaid'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='repayments',
            field=models.ManyToManyField(to='payments.AdminRepayment'),
            preserve_default=True,
        ),
    ]
