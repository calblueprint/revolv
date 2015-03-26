# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_revolvuserprofile_subscribed_to_newsletter'),
        ('payments', '0008_auto_20150202_0048'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminReinvestment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminRepayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(to='base.RevolvUserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='PaymentInstrumentType',
            new_name='PaymentType',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='payment_instrument_type',
            new_name='payment_type',
        ),
    ]
