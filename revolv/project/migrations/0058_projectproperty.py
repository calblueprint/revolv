# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0057_auto_20151018_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=1)),
                ('value', models.CharField(max_length=100)),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
