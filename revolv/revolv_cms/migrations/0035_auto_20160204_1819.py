# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0034_auto_20160204_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revolvcustompage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'size', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'medium', choices=[(b'tiny', b'Tiny'), (b'small', b'Small'), (b'medium', b'Medium'), (b'large', b'Large'), (b'x-large', b'Extra Large'), (b'full_width', b'Full Width')])), (b'layout', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'inline', choices=[(b'img-inline', b'Inline'), (b'img-block', b'Block'), (b'img-left', b'Float Left'), (b'img-right', b'Float Right')]))])), (b'rich_list', wagtail.wagtailcore.blocks.StructBlock([(b'list_content', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock([(b'display_type', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'li_block', choices=[(b'li_block', b'Block'), (b'li_inline', b'Inline'), (b'li_row', b'Row'), (b'li_col', b'Column')])), (b'main_axis', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'm_start', choices=[(b'm_start', b'Start'), (b'm_end', b'End'), (b'm_center', b'Center'), (b'm_space_between', b'Space Between'), (b'm_space_around', b'Space Around')])), (b'perpendicular_axis', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'p_start', choices=[(b'p_start', b'Start'), (b'p_end', b'End'), (b'p_center', b'Center'), (b'p_baseline', b'Baseline'), (b'p_stretch', b'Stretch')])), (b'content', wagtail.wagtailcore.blocks.StreamBlock([(b'rich_text', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'size', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'medium', choices=[(b'tiny', b'Tiny'), (b'small', b'Small'), (b'medium', b'Medium'), (b'large', b'Large'), (b'x-large', b'Extra Large'), (b'full_width', b'Full Width')])), (b'layout', wagtail.wagtailcore.blocks.ChoiceBlock(default=b'inline', choices=[(b'img-inline', b'Inline'), (b'img-block', b'Block'), (b'img-left', b'Float Left'), (b'img-right', b'Float Right')]))]))]))])))]))]),
            preserve_default=True,
        ),
    ]
