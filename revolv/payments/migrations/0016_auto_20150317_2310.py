# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0034_auto_20150317_2310'),
        ('base', '0006_remove_revolvuserprofile_repayments'),
        ('payments', '0015_auto_20150316_0035'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepaymentFragment',
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
        migrations.RemoveField(
            model_name='repayment',
            name='admin_repayment',
        ),
        migrations.RemoveField(
            model_name='repayment',
            name='project',
        ),
        migrations.RemoveField(
            model_name='repayment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Repayment',
        ),
    ]
