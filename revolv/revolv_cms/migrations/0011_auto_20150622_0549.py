# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0010_auto_20150622_0511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dashboardsettings',
            name='category_preferences_explanation_text',
        ),
        migrations.AddField(
            model_name='dashboardsettings',
            name='category_preferences_explanation_paragraph',
            field=wagtail.wagtailcore.fields.RichTextField(default=b'<p>Your donation to RE-volv has been invested in a revolving fund. Money from the fund is used to place solar equipment on community buildings. Over time, the community pays RE-volv back. These repayments are invested in even more solar projects. A fraction of the repayments from a solar investment originates from your investment. Your preferences directly affect where that chunk of money is invested.</p>', help_text=b"A paragraph which will appear below the category preference options on the 'My Impact' section on the dashboard to explain to the user what category preferences mean."),
            preserve_default=True,
        ),
    ]
