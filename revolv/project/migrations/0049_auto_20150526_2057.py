# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0048_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=ckeditor.fields.RichTextField(help_text=b'This is the body of content that shows up on the project page.', verbose_name=b'Project description'),
        ),
        migrations.AlterField(
            model_name='projectupdate',
            name='date',
            field=models.DateField(help_text=b'What time was the update created?', verbose_name=b'Date of update creation', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='projectupdate',
            name='update_text',
            field=ckeditor.fields.RichTextField(help_text=b'What should be the content of the update?', verbose_name=b'Update content'),
        ),
    ]
