# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0017_comppageteam_final_classification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comppageteam',
            name='group',
            field=models.IntegerField(default=0, verbose_name=b'Division'),
        ),
    ]
