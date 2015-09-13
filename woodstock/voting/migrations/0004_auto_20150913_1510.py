# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from uuslug import uuslug


EVENTS = ['MozFest 2015',
          'All Hands 2015',
          'Leadership Summit 2016']


def add_events(apps, schema_editor):
    Event = apps.get_model('voting', 'Event')
    for event_name in EVENTS:
        if not Event.objects.filter(name=event_name).exists():
            event = Event(name=event_name)
            event.slug = uuslug(event_name, event)
            event.save()


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20150911_0957'),
    ]

    operations = [
        migrations.RunPython(add_events)
    ]
