# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0020_payment_user_reinvestment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProjectMontlyRepaymentConfigManager',
        ),
    ]
