# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailembeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0020_auto_20180317_1155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogindexpage',
            options={'verbose_name': 'Blog'},
        ),
        migrations.AlterModelOptions(
            name='blogpage',
            options={'verbose_name': 'Blog post'},
        ),
        migrations.AlterModelOptions(
            name='compindexpage',
            options={'verbose_name': 'Regional page'},
        ),
        migrations.AlterModelOptions(
            name='comppage',
            options={'verbose_name': 'Competition'},
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': 'Home'},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': 'Player'},
        ),
        migrations.AlterModelOptions(
            name='simplepage',
            options={'verbose_name': 'Plain page'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['region__title', 'name'], 'verbose_name': 'Team'},
        ),
        migrations.AddField(
            model_name='team',
            name='region',
            field=models.ForeignKey(related_name='region_teams', on_delete=django.db.models.deletion.SET_NULL, to='business.CompIndexPage', null=True),
        ),
        migrations.AlterField(
            model_name='comppage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([(b'paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), (b'image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock()), (b'caption', wagtail.wagtailcore.blocks.CharBlock(required=False))])), (b'embed', wagtail.wagtailembeds.blocks.EmbedBlock(icon=b'media')), (b'quote', wagtail.wagtailcore.blocks.StructBlock([(b'quote', wagtail.wagtailcore.blocks.CharBlock(required=True)), (b'author', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'author_title', wagtail.wagtailcore.blocks.CharBlock(required=False)), (b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False))]))], blank=True),
        ),
    ]
