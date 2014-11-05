# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_data(apps, schema_editor):
    PaymentInstrumentType = apps.get_model("payments", "PaymentInstrumentType")

    PaymentInstrumentType.objects.create(name="paypal")


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]
