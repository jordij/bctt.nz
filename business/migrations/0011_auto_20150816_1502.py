# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import modelcluster.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0010_auto_20150816_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompPageResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('team_one_games', models.IntegerField(default=0)),
                ('team_two_games', models.IntegerField(default=0)),
                ('page', modelcluster.fields.ParentalKey(related_name='related_results', to='business.CompPage')),
                ('team_one', models.ForeignKey(related_name='competitions_as_one', on_delete=django.db.models.deletion.SET_NULL, to='business.Team', null=True)),
                ('team_two', models.ForeignKey(related_name='competitions_as_two', on_delete=django.db.models.deletion.SET_NULL, to='business.Team', null=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name=b'Post date'),
            preserve_default=True,
        ),
    ]
