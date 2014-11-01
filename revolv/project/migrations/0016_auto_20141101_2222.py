# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_auto_20141031_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='impact_power',
            field=models.FloatField(help_text=b'What is the expected output in killowatts of the proposed solar array?', verbose_name=b'Expected Killowatt Output'),
        ),
        migrations.AlterField(
            model_name='project',
            name='org_name',
            field=models.CharField(help_text=b'What is the name of the organization being helped?', max_length=255, verbose_name=b'Organization Name'),
        ),
    ]
