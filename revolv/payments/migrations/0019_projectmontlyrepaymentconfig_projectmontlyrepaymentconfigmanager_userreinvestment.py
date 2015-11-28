# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_revolvuserprofile_subscribed_to_updates'),
        ('project', '0058_projectproperty'),
        ('payments', '0018_auto_20150320_0712'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectMontlyRepaymentConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveSmallIntegerField(default=2015)),
                ('repayment_type', models.CharField(max_length=3, choices=[(b'SSF', b'Solar Seed Fund'), (b'REV', b'RE-volv Overhead')])),
                ('amount', models.FloatField()),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectMontlyRepaymentConfigManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserReinvestment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(to='project.Project')),
                ('user', models.ForeignKey(to='base.RevolvUserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
