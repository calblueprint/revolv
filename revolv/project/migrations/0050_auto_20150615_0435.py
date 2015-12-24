# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0049_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyOrganizationalCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('amount', models.DecimalField(max_digits=8, decimal_places=3)),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MonthlyReinvestableAmount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('amount', models.DecimalField(max_digits=8, decimal_places=3)),
                ('project', models.ForeignKey(to='project.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='donationlevel',
            name='amount',
            field=models.DecimalField(max_digits=15, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=ckeditor.fields.RichTextField(help_text=b'This is the body of content that shows up on the project page.', verbose_name=b'Project description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectupdate',
            name='date',
            field=models.DateField(help_text=b'What time was the update created?', verbose_name=b'Date of update creation', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectupdate',
            name='update_text',
            field=ckeditor.fields.RichTextField(help_text=b'What should be the content of the update?', verbose_name=b'Update content'),
            preserve_default=True,
        ),
    ]
