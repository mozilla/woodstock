# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0005_auto_20150914_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='apllication_complete',
            new_name='application_complete',
        ),
    ]
