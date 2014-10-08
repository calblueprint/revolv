# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                                        auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=50)),
                ('projects', models.ManyToManyField(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
