# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_data(apps, schema_editor):
    PaymentType = apps.get_model("payments", "PaymentType")

    PaymentType.objects.create(name="stripe")


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0023_tip'),
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]
