# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0012_auto_20150816_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='excerpt',
            field=models.TextField(help_text=b'The excerpt is used on the homepage miniatures only.', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='intro',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
            preserve_default=True,
        ),
    ]
