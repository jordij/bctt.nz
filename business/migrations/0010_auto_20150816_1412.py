# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_auto_20150815_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompPageTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('group', models.IntegerField(default=0)),
                ('page', modelcluster.fields.ParentalKey(related_name='related_teams', to='business.CompPage')),
                ('team', models.ForeignKey(related_name='competitions', on_delete=django.db.models.deletion.SET_NULL, to='business.Team', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comppage',
            name='current',
            field=models.BooleanField(default=False, help_text=b'Is this the current competition?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comppage',
            name='winner',
            field=models.ForeignKey(related_name='winner_of', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='business.Team', null=True),
            preserve_default=True,
        ),
    ]
