# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_project_tagline'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonationLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('amount', models.DecimalField(max_digits=15, decimal_places=2)),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='project',
            name='cover_photo',
            field=imagekit.models.fields.ProcessedImageField(default=None, help_text=b'Choose a beautiful high resolution image to represent this project.', upload_to=b'covers/'),
        ),
    ]
