# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0016_auto_20151010_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='comppageteam',
            name='final_classification',
            field=models.IntegerField(default=0, help_text=b'To set once the comp is finished'),
        ),
    ]
