# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0015_auto_20150823_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='comppageresult',
            name='is_final',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='menuelement',
            name='link_email',
            field=models.EmailField(help_text=b'Set the recipient email address if you want the link to send an email.', max_length=254, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='pagecarouselitem',
            name='link_email',
            field=models.EmailField(help_text=b'Set the recipient email address if you want the link to send an email.', max_length=254, null=True, blank=True),
        ),
    ]
