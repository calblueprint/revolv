# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('revolv_cms', '0003_mainpagesettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='FooterSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_heading', models.CharField(default=b'Contact', help_text=b"The heading to display in the footer menu above the contact information. Probably just 'Contact'", max_length=50)),
                ('contact_email', models.EmailField(default=b'info@re-volv.org', help_text=b'The email address to display in the contact info section of the footer menu.', max_length=200)),
                ('contact_phone_number', models.CharField(default=b'415.314.7719', help_text=b'The phone number to display in the contact info section of the footer menu. e.g. 415.314.7719', max_length=30)),
                ('contact_address_line_1', models.CharField(default=b'972 Mission St. Suite 500', help_text=b'The first line of the address to display in the contact info section of the footer menu.', max_length=150)),
                ('contact_address_line_2', models.CharField(default=b'San Francisco, CA 94103', help_text=b'The second line of the address to display in the contact info section of the footer menu.', max_length=150)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
