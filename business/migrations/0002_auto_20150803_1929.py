# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pagecarouselitem',
            old_name='caption',
            new_name='button',
        ),
    ]
