# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0019_auto_20180316_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitformfield',
            name='choices',
            field=models.TextField(help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', verbose_name='choices', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='field_type',
            field=models.CharField(max_length=16, verbose_name='field type', choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')]),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='to_address',
            field=models.CharField(help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name='to address', blank=True),
        ),
    ]
