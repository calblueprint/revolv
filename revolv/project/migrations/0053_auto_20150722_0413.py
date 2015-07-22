# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from revolv.project.models import Category


def remove_geographic_category(apps, schema_editor):
    Category.objects.get_or_create(title='Geographic')[0].delete()


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0052_auto_20150630_2238'),
    ]

    operations = [
        migrations.RunPython(remove_geographic_category),
    ]
