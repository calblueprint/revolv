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
            name='post_funding_updates',
            field=models.TextField(default=b'No Updates Available', help_text=b'Add any post project completion updates you want to let your backers know about.', verbose_name=b'Updates After Completion'),
            preserve_default=True,
        ),
    ]
