# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_id', models.IntegerField(default=0)),
                ('number_of_events', models.IntegerField(default=1)),
                ('reasoning', models.TextField(default=b'', blank=True)),
                ('contributions', models.TextField(default=b'', blank=True)),
                ('learning_areas', models.TextField(default=b'', blank=True)),
                ('recommendation_letter', models.CharField(default=b'', max_length=255, blank=True)),
                ('ideas', models.TextField(default=b'', blank=True)),
                ('commitments', models.TextField(default=b'', blank=True)),
                ('functional_team', models.CharField(default=b'', max_length=255, blank=True)),
                ('team_contact', models.CharField(default=b'', max_length=255, blank=True)),
                ('participation_opportunities', models.TextField(default=b'', blank=True)),
                ('tracking_communities', models.TextField(default=b'', blank=True)),
                ('community_record', models.TextField(default=b'', blank=True)),
                ('community_impact', models.TextField(default=b'', blank=True)),
                ('other', models.TextField(default=b'', blank=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('apllication_complete', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreferredEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preferred', models.BooleanField(default=False)),
                ('reason', models.TextField(default=b'', blank=True)),
                ('application', models.ForeignKey(to='voting.Application')),
                ('event', models.ForeignKey(to='voting.Event')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='application',
            name='event',
            field=models.ManyToManyField(to='voting.Event', through='voting.PreferredEvent'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mozillianprofile',
            name='application',
            field=models.ForeignKey(related_name='applications', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='voting.Application', null=True),
            preserve_default=True,
        ),
    ]
