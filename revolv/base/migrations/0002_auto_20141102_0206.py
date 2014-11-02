# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_data(apps, schema_editor):
    Permission = apps.get_model("django.contrib.auth", "Permission")
    Group = apps.get_model("django.contrib.auth", "Group")

    # the following should match the data in base.fixtures
    amb_perm = Permission.objects.create(codename="revolv_ambassador", name="Is Re-volv Ambassador")
    ad_perm = Permission.objects.create(codename="revolv_admin", name="Is Re-volv Admin")

    admins = Group.objects.create(name="Re-volv Admins")
    ambassadors = Group.objects.create(name="Re-volv Solar Abassadors")
    admins.add_perm(ad_perm, amb_perm)
    ambassadors.add_perm(amb_perm)


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_data)
    ]
