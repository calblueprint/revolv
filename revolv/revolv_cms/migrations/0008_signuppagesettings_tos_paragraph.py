# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0007_paymentmodalsettings_confirm_payment_paragraph'),
    ]

    operations = [
        migrations.AddField(
            model_name='signuppagesettings',
            name='tos_paragraph',
            field=wagtail.wagtailcore.fields.RichTextField(default=b"<p>Signing up for an account means joining the RE-volv community and agreeing to the <a href='/tos'>terms of service</a>. RE-volv will never store credit card information and will never give your information to third parties. Welcome!</p>", help_text=b'The paragraph to display directly after the form but before the sign up button. Should include a link to the Terms of Service page.', blank=True),
            preserve_default=True,
        ),
    ]
