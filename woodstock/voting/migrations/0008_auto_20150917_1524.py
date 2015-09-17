# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0007_mozillianprofile_reps_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mozillianprofile',
            name='application',
            field=models.ForeignKey(related_name='users', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='voting.Application', null=True),
            preserve_default=True,
        ),
    ]
