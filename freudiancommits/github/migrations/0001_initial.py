# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Repo'
        db.create_table('github_repo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('pushed_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('github', ['Repo'])

        # Adding model 'Issue'
        db.create_table('github_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issues', to=orm['github.Repo'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('assignee', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('resolved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('body', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('github', ['Issue'])

        # Adding unique constraint on 'Issue', fields ['repo', 'number']
        db.create_unique('github_issue', ['repo_id', 'number'])

        # Adding model 'StarredRepo'
        db.create_table('github_starredrepo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(related_name='starred_repos', to=orm['socialaccount.SocialAccount'])),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['github.Repo'])),
        ))
        db.send_create_signal('github', ['StarredRepo'])

        # Adding unique constraint on 'StarredRepo', fields ['account', 'repo']
        db.create_unique('github_starredrepo', ['account_id', 'repo_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'StarredRepo', fields ['account', 'repo']
        db.delete_unique('github_starredrepo', ['account_id', 'repo_id'])

        # Removing unique constraint on 'Issue', fields ['repo', 'number']
        db.delete_unique('github_issue', ['repo_id', 'number'])

        # Deleting model 'Repo'
        db.delete_table('github_repo')

        # Deleting model 'Issue'
        db.delete_table('github_issue')

        # Deleting model 'StarredRepo'
        db.delete_table('github_starredrepo')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'github.issue': {
            'Meta': {'ordering': "('repo__owner', 'repo__name', 'number')", 'unique_together': "(('repo', 'number'),)", 'object_name': 'Issue'},
            'assignee': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': "orm['github.Repo']"}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'github.repo': {
            'Meta': {'ordering': "('owner', 'name')", 'object_name': 'Repo'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'pushed_at': ('django.db.models.fields.DateTimeField', [], {}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        'github.starredrepo': {
            'Meta': {'ordering': "('account__user__username', 'repo__owner', 'repo__name')", 'unique_together': "(('account', 'repo'),)", 'object_name': 'StarredRepo'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'starred_repos'", 'to': "orm['socialaccount.SocialAccount']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['github.Repo']"})
        },
        'socialaccount.socialaccount': {
            'Meta': {'unique_together': "(('provider', 'uid'),)", 'object_name': 'SocialAccount'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_data': ('allauth.socialaccount.fields.JSONField', [], {'default': "'{}'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['github']