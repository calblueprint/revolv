# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0024_auto_20141115_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='solar_url',
            field=models.URLField(help_text=b'This can be found by going to http://home.solarlog-web.net/, going to the         solar log profile for your site, and clicking on the Graphics sub-page. Copy and paste         the URL in the address bar into here.', max_length=255, verbose_name=b'Solar Log Graphics URL', blank=True),
        ),
    ]
