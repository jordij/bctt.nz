# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0022_auto_20180318_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompIndexSponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', modelcluster.fields.ParentalKey(related_name='related_sponsors', to='business.CompIndexPage')),
                ('sponsor', models.ForeignKey(related_name='regions', to='business.Sponsor')),
            ],
        ),
        migrations.AlterModelOptions(
            name='regionalindexpage',
            options={'verbose_name': 'Regions', 'verbose_name_plural': 'Regions'},
        ),
    ]
