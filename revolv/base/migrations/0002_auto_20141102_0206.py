# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_data(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    Group.objects.create(name="administrators")
    Group.objects.create(name="ambassadors")


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data)
    ]
