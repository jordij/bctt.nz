# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks
import wagtail.wagtailcore.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0006_add_verbose_names'),
        ('business', '0005_auto_20150803_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255, blank=True)),
                ('bio', models.TextField(max_length=1020, blank=True)),
                ('image', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),
            ],
            options={
                'verbose_name': 'Author Biography',
                'description': 'Articles authors short bio',
                'verbose_name_plural': 'Author Biographies',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='submitformpage',
            options={'verbose_name': 'Contact form'},
        ),
        migrations.AddField(
            model_name='blogpage',
            name='author',
            field=models.ForeignKey(related_name='articles', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='business.Author', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'heading', wagtail.wagtailcore.blocks.CharBlock(classname=b'full title')), (b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock())]),
            preserve_default=True,
        ),
    ]
