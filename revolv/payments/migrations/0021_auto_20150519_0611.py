# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_revolvuserprofile_preferred_categories'),
        ('payments', '0020_adminexpense_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminAdjustment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(to='base.RevolvUserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='adminexpense',
            name='admin',
        ),
        migrations.DeleteModel(
            name='AdminExpense',
        ),
    ]
