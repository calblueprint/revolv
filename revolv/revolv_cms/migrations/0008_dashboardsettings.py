# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('revolv_cms', '0007_paymentmodalsettings_confirm_payment_paragraph'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('impact_statistics_header_text', models.CharField(default=b'Thank you for contributing! Your contribution has...', help_text=b"The heading above the impact statistics on the dashboard, e.g. 'Thank you for contributing! Your contribution has...'.", max_length=100)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
