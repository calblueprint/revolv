# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0015_add_more_verbose_names'),
        ('revolv_cms', '0002_revolvlinkpage'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainPageSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('site_tagline', models.CharField(default=b"WE'RE SAVING TOMORROW", help_text=b'The tagline for the site, which will be shown large and centered over the animated cover video.', max_length=100)),
                ('site_subheading', models.TextField(default=b"When you donate to RE-volv's solar projects, you are making a lasting impact on the environment and the world around you.", help_text=b'The description text that will be shown after the site tagline - a brief (one sentence) introduction to what RE-volv is and how donors can help.')),
                ('learn_button_text', models.CharField(default=b'Learn about how RE-volv works', help_text=b"The label on the 'Learn more button'. E.g. 'Learn about how RE-volv works'", max_length=50)),
                ('current_project_heading', models.CharField(default=b'OUR CURRENT PROJECT', help_text=b"The heading to display above the featured project on the homepage, e.g. 'Our current project'", max_length=50)),
                ('how_it_works_heading', models.CharField(default=b'HOW RE-VOLV WORKS', help_text=b"The heading to display above the 'Learn about how RE-volv works' section on the homepage, e.g. 'Learn about how RE-volv works'", max_length=50)),
                ('how_it_works_intro', models.TextField(default=b'Climate change is among the most alarming environmental issues the world faces today.', help_text=b"Intro paragraph for the 'Learn about how RE-volv works' section of the homepage.")),
                ('how_it_works_tagline', models.CharField(default=b'How would your donation to RE-volv help?', help_text=b"Large heading directly before the infograph portion of the homepage. e.g. 'How would your donation help?'", max_length=200)),
                ('how_it_works_pitch', models.CharField(default=b'Be a part of something great.', help_text=b"Large text directly before the call to action donation button at the bottom of the hompage, e.g. 'Be part of something great.'", max_length=200)),
                ('call_to_action_button_text', models.CharField(default=b'Start contributing', help_text=b'The label on the green call to action button at the bottom of the homepage.', max_length=50)),
                ('site', models.OneToOneField(editable=False, to='wagtailcore.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
