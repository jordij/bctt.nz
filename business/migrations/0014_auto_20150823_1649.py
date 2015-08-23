# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks
import django.db.models.deletion
import business.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('business', '0013_auto_20150819_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submitformpage',
            name='body',
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='feed_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogindexpage',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blogpage',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='compindexpage',
            name='feed_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='compindexpage',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comppage',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepage',
            name='feed_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepage',
            name='feed_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepage',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submitformpage',
            name='feed_image',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='submitformpage',
            name='subtitle',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', business.blocks.SimpleRichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon=b'media')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'author_title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))]))]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comppage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', business.blocks.SimpleRichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon=b'media')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'author_title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))]))]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='simplepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', business.blocks.SimpleRichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon=b'media')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'author_title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))]))]),
            preserve_default=True,
        ),
    ]
