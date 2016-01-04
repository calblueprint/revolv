# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('revolv_cms', '0029_auto_20151115_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainpagesettings',
            name='how_it_works_video_url',
            field=models.URLField(default=b'https://www.youtube.com/embed/eSADOAxjcPU', help_text=b"URL for 'how it works' video"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainpagesettings',
            name='how_it_works_heading',
            field=models.CharField(default=b'How it works', help_text=b"The heading to display above the 'Learn about how RE-volv works' section on the homepage, e.g. 'Learn about how RE-volv works'", max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mainpagesettings',
            name='how_it_works_intro',
            field=models.TextField(default=b"We believe that everyone should have the ability to support clean energy. So we created a new way for people to take action. It's a pretty simple idea. We raise money through crowdfunding to put solar panels on community-serving nonprofit organizations and worker-owned cooperatives. As these organizations pay us back, we reinvest the money into more solar projects in communities across the country. This creates a revolving fund for solar energy that continually perpetuates itself building more and more solar. It's a pay-it-forward model for community solar. We call it the Solar Seed Fund.", help_text=b"Intro paragraph for the 'Learn about how RE-volv works' section of the homepage."),
            preserve_default=True,
        ),
    ]
