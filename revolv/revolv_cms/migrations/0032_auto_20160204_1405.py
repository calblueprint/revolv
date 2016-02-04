# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0031_auto_20160131_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revolvcustompage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'size', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'medium', choices=[(b'tiny', b'Tiny'), (b'small', b'Small'), (b'medium', b'Medium'), (b'large', b'Large')])), (b'layout', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'inline', choices=[(b'img-inline', b'Inline'), (b'img-block', b'Block'), (b'img-left', b'Float Left'), (b'img-right', b'Float Right')]))]))]),
            preserve_default=True,
        ),
    ]
