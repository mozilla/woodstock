# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0006_auto_20150914_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='mozillianprofile',
            name='reps_display_name',
            field=models.CharField(default=b'', max_length=255),
            preserve_default=True,
        ),
    ]
