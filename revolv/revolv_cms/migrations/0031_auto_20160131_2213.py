# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0030_auto_20160104_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainpagesettings',
            name='learn_button_text',
            field=models.CharField(default=b'DONATE', help_text=b"The label on the 'Learn more button'. E.g. 'Learn about how RE-volv works'", max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainpagesettings',
            name='site_tagline',
            field=models.CharField(default=b'STOP IMAGINING<i></i> A CLEAN ENERGY FUTURE. START CREATING IT.', help_text=b'The tagline for the site, which will be shown large and centered over the animated cover video.', max_length=100),
            preserve_default=True,
        ),
    ]
