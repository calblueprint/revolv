# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0038_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='YearlyEscalatorRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('amount', models.DecimalField(max_digits=5, decimal_places=4)),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='project',
            name='internal_rate_return',
            field=models.DecimalField(default=0.0, help_text=b'The internal rate of return for this project.', verbose_name=b'Internal Rate of Return', max_digits=6, decimal_places=4),
        ),
    ]
