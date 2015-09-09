# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MozillianGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MozillianProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(max_length=100, blank=True)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(default=b'', max_length=75)),
                ('city', models.CharField(default=b'', max_length=50, blank=True)),
                ('country', models.CharField(default=b'', max_length=50)),
                ('ircname', models.CharField(default=b'', max_length=50)),
                ('avatar_url', models.URLField(default=b'', max_length=400)),
                ('bio', models.TextField(default=b'', blank=True)),
                ('username', models.CharField(default=b'', max_length=100)),
                ('tracking_groups', models.ManyToManyField(related_name='mozillians_tracking', to='voting.MozillianGroup')),
            ],
            options={
                'ordering': ['country', 'full_name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.IntegerField(default=0, choices=[(0, b'Skip'), (1, b'Probably'), (2, b'Definitely'), (-1, b'No')])),
                ('nominee', models.ForeignKey(related_name='votes', to='voting.MozillianProfile')),
                ('voter', models.ForeignKey(related_name='user_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
