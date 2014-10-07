# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('funding_goal', models.DecimalField(max_digits=15, decimal_places=2)),
                ('title', models.CharField(max_length=255)),
                ('video_url', models.URLField(max_length=255)),
                ('impact_power', models.FloatField()),
                ('location', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('end_date', models.DateTimeField()),
                ('project_status', models.CharField(default=b'PR', max_length=2, choices=[(b'AC', b'Accepted'), (b'PR', b'Proposed'), (b'CO', b'Completed'), (b'BU', b'Building')])),
                ('mission_statement', models.CharField(max_length=5000)),
                ('cover_photo', models.URLField(max_length=255)),
                ('org_start_date', models.DateField()),
                ('actual_energy', models.FloatField()),
                ('amount_repaid', models.DecimalField(max_digits=15, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
