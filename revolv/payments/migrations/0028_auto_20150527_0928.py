# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0027_auto_20150526_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminadjustment',
            name='amount',
            field=models.FloatField(verbose_name=b'How many dollars is this transaction?'),
        ),
        migrations.AlterField(
            model_name='adminadjustment',
            name='cash_type',
            field=models.CharField(default=b'cash_out', max_length=10, verbose_name=b'Is this income or an expense?', choices=[(b'cash_in', b'Income'), (b'cash_out', b'Expense')]),
        ),
        migrations.AlterField(
            model_name='adminadjustment',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2015, 5, 27, 9, 28, 30, 31883), verbose_name=b'What time period should this transaction be recorded under?'),
        ),
        migrations.AlterField(
            model_name='adminadjustment',
            name='name',
            field=models.CharField(max_length=100, verbose_name=b'What is the name of this expense or income?'),
        ),
    ]
