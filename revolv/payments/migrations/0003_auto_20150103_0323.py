# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_data(apps, schema_editor):
    PaymentInstrumentType = apps.get_model("payments", "PaymentInstrumentType")

    PaymentInstrumentType.objects.create(name="reinvestment")
    PaymentInstrumentType.objects.create(name="check")
    PaymentInstrumentType.objects.create(name="repayment")


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_auto_20141105_0451'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]
