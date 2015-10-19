# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0024_auto_20151011_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activeprojectspagesettings',
            name='multiple_projects_heading',
            field=models.CharField(default=b'OUR CURRENT PROJECTS', help_text=b"The heading to display above the featured project on the projects list when there are multiple active projects, e.g. 'Our current projects'", max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activeprojectspagesettings',
            name='start_funding_button_text',
            field=models.CharField(default=b'Create a new project', help_text=b'The label on the green call to action button at the bottom of the homepage.', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainpagesettings',
            name='multiple_projects_heading',
            field=models.CharField(default=b'OUR CURRENT PROJECTS', help_text=b"The heading to display above the featured project on the homepage when there are multiple featured projects, e.g. 'Our current projects'", max_length=50),
            preserve_default=True,
        ),
    ]
