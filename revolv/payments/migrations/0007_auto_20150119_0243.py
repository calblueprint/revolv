# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20150118_2217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donation',
            name='payment_transaction',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='project',
        ),
        migrations.DeleteModel(
            name='Donation',
        ),
        migrations.RemoveField(
            model_name='paymenttransaction',
            name='payment_instrument_type',
        ),
        migrations.RemoveField(
            model_name='paymenttransaction',
            name='user',
        ),
        migrations.DeleteModel(
            name='PaymentTransaction',
        ),
    ]
