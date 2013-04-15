# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MozillianGroup'
        db.create_table(u'voting_mozilliangroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'voting', ['MozillianGroup'])

        # Adding model 'MozillianProfile'
        db.create_table(u'voting_mozillianprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, blank=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(default='', max_length=75)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('country', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('ircname', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('avatar_url', self.gf('django.db.models.fields.URLField')(default='', max_length=400)),
            ('bio', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'voting', ['MozillianProfile'])

        # Adding M2M table for field tracking_groups on 'MozillianProfile'
        db.create_table(u'voting_mozillianprofile_tracking_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mozillianprofile', models.ForeignKey(orm[u'voting.mozillianprofile'], null=False)),
            ('mozilliangroup', models.ForeignKey(orm[u'voting.mozilliangroup'], null=False))
        ))
        db.create_unique(u'voting_mozillianprofile_tracking_groups', ['mozillianprofile_id', 'mozilliangroup_id'])

        # Adding model 'Vote'
        db.create_table(u'voting_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('voter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('nominee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['voting.MozillianProfile'])),
            ('vote', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'voting', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'MozillianGroup'
        db.delete_table(u'voting_mozilliangroup')

        # Deleting model 'MozillianProfile'
        db.delete_table(u'voting_mozillianprofile')

        # Removing M2M table for field tracking_groups on 'MozillianProfile'
        db.delete_table('voting_mozillianprofile_tracking_groups')

        # Deleting model 'Vote'
        db.delete_table(u'voting_vote')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'voting.mozilliangroup': {
            'Meta': {'ordering': "['name']", 'object_name': 'MozillianGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'voting.mozillianprofile': {
            'Meta': {'ordering': "['country', 'full_name']", 'object_name': 'MozillianProfile'},
            'avatar_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '400'}),
            'bio': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'default': "''", 'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ircname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'}),
            'tracking_groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'mozillians_tracking'", 'symmetrical': 'False', 'to': u"orm['voting.MozillianGroup']"})
        },
        u'voting.vote': {
            'Meta': {'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nominee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['voting.MozillianProfile']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'voter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['voting']