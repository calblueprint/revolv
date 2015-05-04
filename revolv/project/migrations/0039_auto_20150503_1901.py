# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from revolv.project.models import Category


def add_initial_categories(apps, schema_editor):
    for title in Category.valid_categories:
        Category.objects.get_or_create(title=title)


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0038_merge'),
    ]

    operations = [
        migrations.RunPython(add_initial_categories),
    ]
