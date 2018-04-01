# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0018_auto_20151107_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon=b'media')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'author_title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))]))]),
        ),
        migrations.AlterField(
            model_name='comppage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon=b'media')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'author_title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))]))]),
        ),
        migrations.AlterField(
            model_name='simplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon=b'media')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'author_title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))]))]),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='choices',
            field=models.CharField(help_text='Comma separated list of choices. Only applicable in checkboxes, radio and dropdown.', max_length=512, verbose_name='choices', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='default_value',
            field=models.CharField(help_text='Default value. Comma separated values supported for checkboxes.', max_length=255, verbose_name='default value', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='field_type',
            field=models.CharField(max_length=16, verbose_name='field type', choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time')]),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='help_text',
            field=models.CharField(max_length=255, verbose_name='help text', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='label',
            field=models.CharField(help_text='The label of the form field', max_length=255, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='submitformfield',
            name='required',
            field=models.BooleanField(default=True, verbose_name='required'),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='from_address',
            field=models.CharField(max_length=255, verbose_name='from address', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='subject',
            field=models.CharField(max_length=255, verbose_name='subject', blank=True),
        ),
        migrations.AlterField(
            model_name='submitformpage',
            name='to_address',
            field=models.CharField(help_text='Optional - form submissions will be emailed to this address', max_length=255, verbose_name='to address', blank=True),
        ),
    ]
