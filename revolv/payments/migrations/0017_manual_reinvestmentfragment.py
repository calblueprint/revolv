# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_data(apps, schema_editor):
    PaymentType = apps.get_model("payments", "PaymentType")

    PaymentType.objects.all().delete()
    PaymentType.objects.create(name='paypal', pk=0)
    PaymentType.objects.create(name='reinvestment_fragment', pk=1)
    PaymentType.objects.create(name='check', pk=2)


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0016_auto_20150317_2310'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]
