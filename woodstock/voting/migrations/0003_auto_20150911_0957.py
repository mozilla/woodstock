# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0002_auto_20150910_0652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mozillianprofile',
            old_name='username',
            new_name='mozillian_username',
        ),
    ]
