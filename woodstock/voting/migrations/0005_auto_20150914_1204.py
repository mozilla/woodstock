# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0004_auto_20150913_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='commitments',
            new_name='commitment_1',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='community_record',
            new_name='commitment_2',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='contributions',
            new_name='commitment_3',
        ),
        migrations.RenameField(
            model_name='application',
            old_name='tracking_communities',
            new_name='community',
        ),
        migrations.AddField(
            model_name='application',
            name='impact',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='track_record',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
