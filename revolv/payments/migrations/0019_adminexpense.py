# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_revolvuserprofile_preferred_categories'),
        ('payments', '0018_auto_20150320_0712'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminExpense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(to='base.RevolvUserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
