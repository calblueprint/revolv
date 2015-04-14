# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0028_remove_project_amount_repaid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('update_text', models.TextField(help_text=b'What does the update say?', verbose_name=b'Text of the update')),
                ('date', models.DateField(help_text=b'What time was your update created?', verbose_name=b'Date of update creation', auto_now_add=True)),
                ('project', models.ForeignKey(related_name=b'update', to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
