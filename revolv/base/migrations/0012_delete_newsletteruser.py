# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_newsletteruser_subscribed_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NewsletterUser',
        ),
    ]
