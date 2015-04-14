# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_revolvuserprofile_reinvest_pool'),
        ('project', '0031_merge'),
        ('payments', '0012_auto_20150315_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin_repayment', models.ForeignKey(to='payments.AdminRepayment')),
                ('project', models.ForeignKey(to='project.Project')),
                ('user', models.ForeignKey(to='base.RevolvUserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='adminreinvestment',
            new_name='admin_reinvestment',
        ),
    ]
