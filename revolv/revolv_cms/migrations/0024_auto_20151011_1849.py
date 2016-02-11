# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('revolv_cms', '0023_auto_20150802_0456'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveProjectsPageSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('join_the_movement', models.CharField(default=b'Join the movement.', help_text=b"Large text directly before the call to action donation button at the bottom of the projects page, e.g. 'Join the movement.'", max_length=200)),
                ('start_funding_button_text', models.CharField(default=b'Contact Us to Fund a New Project', help_text=b'The label on the green call to action button at the bottom of the homepage.', max_length=50)),
                ('single_project_heading', models.CharField(default=b'OUR CURRENT PROJECT', help_text=b"The heading to display above the featured project on the projects list page when there is only one active project, e.g. 'Our current project'", max_length=50)),
                ('multiple_projects_heading', models.CharField(default=b'OUR CURRENT PROJECTS', help_text=b"The heading to display above the featured project on the projects list when there are multiple active projects, e.g. 'Our current project'", max_length=50)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='mainpagesettings',
            name='current_project_heading',
        ),
        migrations.AddField(
            model_name='mainpagesettings',
            name='multiple_projects_heading',
            field=models.CharField(default=b'OUR CURRENT PROJECTS', help_text=b"The heading to display above the featured project on the homepage when there are multiple featured projects, e.g. 'Our current project'", max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mainpagesettings',
            name='single_project_heading',
            field=models.CharField(default=b'OUR CURRENT PROJECT', help_text=b"The heading to display above the featured project on the homepage when there is only one featured project, e.g. 'Our current project'", max_length=50),
            preserve_default=True,
        ),
    ]
