# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('revolv_cms', '0004_footersettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginPageSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(default=b'Welcome back!', help_text=b"The heading text of the login page. e.g. 'Welcome back!'", max_length=50)),
                ('heading_for_donation', models.CharField(default=b'Login to donate', help_text=b"The heading text of the login page when specifically directed there as a consequence of clicking a donate button when not logged in. e.g. 'Please log in to donate'", max_length=30)),
                ('login_paragraph', wagtail.wagtailcore.fields.RichTextField(default=b"<p>Log in to see the impact you've had on communities that use renewable solar energy.</p>", help_text=b'The paragraph of text to be shown under the heading on the login page, but before the links to the register page and the forgot password page.')),
                ('login_paragraph_for_donation', wagtail.wagtailcore.fields.RichTextField(default=b'', help_text=b'The paragraph of text to be shown under the heading on the login page, but specifically when the user is directed to the login page as a result of clicking a donate button when not logged in.')),
                ('button_text', models.CharField(default=b'Log in', help_text=b"The text on the actual login button, e.g. 'Log in'", max_length=30)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PaymentModalSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment_modal_paragraph', wagtail.wagtailcore.fields.RichTextField(default=b'', help_text=b'Optional: a paragraph which will appear above the credit card entry areas of the donation modal on the project page. Use this as another opportunity to assure the user of the security of the payments.')),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectPageSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('donors_wording', models.CharField(default=b'donors', help_text=b"The wording that will be displayed after the number of donors to the project the use is viewing. For example, 'donors' or 'contributors'.", max_length=20)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignupPageSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(default=b'Welcome!', help_text=b"The heading text of the sign up page. e.g. 'Welcome!'", max_length=50)),
                ('signup_paragraph', wagtail.wagtailcore.fields.RichTextField(default=b'<p>Start investing in renewable solar energy by signing up for an account.</p>', help_text=b'The paragraph of text to be shown under the heading on the sign up page, but before the link to the login page.')),
                ('button_text', models.CharField(default=b'Sign Up', help_text=b"The text on the actual sign up button, e.g. 'Sign up'", max_length=30)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
