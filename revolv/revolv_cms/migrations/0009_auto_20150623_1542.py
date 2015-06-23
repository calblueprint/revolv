# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('revolv_cms', '0008_signuppagesettings_tos_paragraph'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectStatisticsSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kilowatt_description', models.CharField(default=b'Kilowatt power output', help_text=b"A description of the concept of kilowatts of power that a project generates, to be displayed as a statistic on the dashboard or project pages. e.g. 'Kilowatt power output'", max_length=50)),
                ('dollars_saved_description', models.CharField(default=b'Dollars saved per month', help_text=b"A description of the dollars that a project will save in elctricity costs per month, to be displayed as a statistic on the dashboard or project pages. e.g. 'Dollars saved per month'", max_length=50)),
                ('carbon_saved_description', models.CharField(default=b'Carbon emissions saved per month', help_text=b"A description of the pounds of carbon that will be saved by a project per month, to be displayed as a statistic on the dashboard or project pages. e.g. 'Carbon emissions saved per month'", max_length=50)),
                ('trees_description', models.CharField(default=b'Equivalent carbon savings of trees', help_text=b"A description of the acres of trees which, if planted, would provide equivalent savings to a project, to be displayed as a statistic on the dashboard or project pages. e.g. 'Equivalent carbon savings in trees'", max_length=50)),
                ('automobile_miles_description', models.CharField(default=b'Equivalent carbon in automobile miles', help_text=b"A description of the equivalent automobile miles which, if driven, would produce the same amount of carbon that a project will save per month, to be displayed as a statistic on the dashboard or project pages. e.g. 'Equivalent carbon in automobile miles'", max_length=50)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='signuppagesettings',
            name='tos_paragraph',
            field=wagtail.wagtailcore.fields.RichTextField(default=b"<p>Signing up for an account means joining the RE-volv community and agreeing to the <a href='/tos/'>terms of service</a>. RE-volv will never store credit card information and will never give your information to third parties. Welcome!</p>", help_text=b'The paragraph to display directly after the form but before the sign up button. Should include a link to the Terms of Service page.', blank=True),
            preserve_default=True,
        ),
    ]
