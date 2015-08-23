# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0014_auto_20150823_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpagerelatedlink',
            name='link_document',
        ),
        migrations.RemoveField(
            model_name='blogpagerelatedlink',
            name='link_email',
        ),
        migrations.RemoveField(
            model_name='blogpagerelatedlink',
            name='link_external',
        ),
        migrations.RemoveField(
            model_name='blogpagerelatedlink',
            name='link_phone',
        ),
        migrations.RemoveField(
            model_name='blogpagerelatedlink',
            name='title',
        ),
        migrations.AlterField(
            model_name='blogpagerelatedlink',
            name='link_page',
            field=models.ForeignKey(related_name='+', default=1, to='business.BlogPage'),
            preserve_default=False,
        ),
    ]
