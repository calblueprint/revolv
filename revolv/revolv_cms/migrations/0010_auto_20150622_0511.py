# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0009_auto_20150622_0303'),
    ]

    operations = [
        migrations.AddField(
            model_name='dashboardsettings',
            name='category_preferences_explanation_header_text',
            field=models.CharField(default=b"What's going on?", help_text=b"The header of the category preference explanation in the 'My Impact' section of the dashboard.", max_length=50),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardsettings',
            name='category_preferences_explanation_text',
            field=wagtail.wagtailcore.fields.RichTextField(default=b'Your donation to RE-volv has been invested in a revolving fund. Money from the fund is used to place solar equipment on community buildings. Over time, the community pays RE-volv back. These repayments are invested in even more solar projects. A fraction of the repayments from a solar investment originates from your investment. Your preferences directly affect where that chunk of money is invested.', help_text=b"A paragraph which will appear below the category preference options on the 'My Impact' section on the dashboard to explain to the user what category preferences mean."),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardsettings',
            name='category_preferences_header_text',
            field=models.CharField(default=b'What type of projects should we invest your repayments in next?', help_text=b"The heading of category preferences section in the 'My Impact' section of the dashboard.", max_length=100),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dashboardsettings',
            name='last_statistic_description_text',
            field=models.CharField(default=b'Help us save the world by going solar!', help_text=b"The description of the bottom right icon on the 'My Impact' section of the dashboard.", max_length=100),
            preserve_default=True,
        ),
    ]
