# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_payment_paymentmanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentManager',
        ),
    ]
