# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20150803_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagecarouselitem',
            name='content',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
    ]
