# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import wagtail.wagtailcore.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0006_auto_20150616_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentmodalsettings',
            name='confirm_payment_paragraph',
            field=wagtail.wagtailcore.fields.RichTextField(default=b'', help_text=b'Optional: a paragraph which will appear above the submit button of the donation confirmation modal on the project page. Use this as another opportunity to assure the user of the security of the payments.', blank=True),
            preserve_default=True,
        ),
    ]
