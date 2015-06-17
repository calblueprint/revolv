# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0005_loginpagesettings_paymentmodalsettings_projectpagesettings_signuppagesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footersettings',
            name='contact_address_line_2',
            field=models.CharField(default=b'San Francisco, CA 94103', help_text=b'The second line of the address to display in the contact info section of the footer menu.', max_length=150, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loginpagesettings',
            name='login_paragraph',
            field=wagtail.wagtailcore.fields.RichTextField(default=b"<p>Log in to see the impact you've had on communities that use renewable solar energy.</p>", help_text=b'The paragraph of text to be shown under the heading on the login page, but before the links to the register page and the forgot password page.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='loginpagesettings',
            name='login_paragraph_for_donation',
            field=wagtail.wagtailcore.fields.RichTextField(default=b'', help_text=b'The paragraph of text to be shown under the heading on the login page, but specifically when the user is directed to the login page as a result of clicking a donate button when not logged in.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='paymentmodalsettings',
            name='payment_modal_paragraph',
            field=wagtail.wagtailcore.fields.RichTextField(default=b'', help_text=b'Optional: a paragraph which will appear above the credit card entry areas of the donation modal on the project page. Use this as another opportunity to assure the user of the security of the payments.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='signuppagesettings',
            name='signup_paragraph',
            field=wagtail.wagtailcore.fields.RichTextField(default=b'<p>Start investing in renewable solar energy by signing up for an account.</p>', help_text=b'The paragraph of text to be shown under the heading on the sign up page, but before the link to the login page.', blank=True),
            preserve_default=True,
        ),
    ]
