# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0012_auto_20141030_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_date',
            field=models.DateField(help_text=b'When will this crowdfunding project end?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='impact_power',
            field=models.FloatField(help_text=b'What is the expected output in killowatts of the proposed solar array.', verbose_name=b'Expected KilloWatt Output'),
        ),
        migrations.AlterField(
            model_name='project',
            name='location',
            field=models.CharField(help_text=b'What is the address of the organization where the solar panels will be installed?', max_length=255, verbose_name=b'Organization Address'),
        ),
        migrations.AlterField(
            model_name='project',
            name='org_start_date',
            field=models.DateField(help_text=b'When was the organization being helped established?', null=True, verbose_name=b'Organization Founding Date', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(help_text=b'How would you like to title this project?', max_length=255),
        ),
    ]
