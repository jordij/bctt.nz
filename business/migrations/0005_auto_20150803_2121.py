# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0001_squashed_0016_change_page_url_path_to_text_field'),
        ('business', '0004_auto_20150803_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitFormField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('label', models.CharField(help_text='The label of the form field', max_length=255, verbose_name='Label')),
                ('field_type', models.CharField(max_length=16, verbose_name='Field type', choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')])),
                ('required', models.BooleanField(default=True, verbose_name='Required')),
                ('choices', models.CharField(help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', max_length=512, verbose_name='Choices', blank=True)),
                ('default_value', models.CharField(help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='Default value', blank=True)),
                ('help_text', models.CharField(max_length=255, verbose_name='Help text', blank=True)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubmitFormPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('to_address', models.CharField(help_text='Optional - form submissions will be emailed to this address', max_length=255, verbose_name='To address', blank=True)),
                ('from_address', models.CharField(max_length=255, verbose_name='From address', blank=True)),
                ('subject', models.CharField(max_length=255, verbose_name='Subject', blank=True)),
                ('body', wagtail.wagtailcore.fields.RichTextField(help_text=b'Edit the content you want to see before the form.', blank=True)),
                ('thank_you_text', wagtail.wagtailcore.fields.RichTextField(help_text=b'Set the message users will see after submitting the form.', blank=True)),
            ],
            options={
                'verbose_name': 'Add a site page',
                'description': 'Page with the form to submit a new Wagtail site',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='submitformfield',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='form_fields', to='business.SubmitFormPage'),
            preserve_default=True,
        ),
    ]
