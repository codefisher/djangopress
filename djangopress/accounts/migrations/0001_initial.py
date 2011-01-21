# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='New member', max_length=100)),
            ('homepage', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('signature', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('registration_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True)),
            ('last_ip_used', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True)),
            ('admin_note', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('activate_key', self.gf('django.db.models.fields.CharField')(max_length=127, null=True, blank=True)),
            ('activate_key_expirary', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('banned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('remember_between_visits', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])

        # Adding M2M table for field properties on 'UserProfile'
        db.create_table('accounts_userprofile_properties', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False)),
            ('property', models.ForeignKey(orm['util.property'], null=False))
        ))
        db.create_unique('accounts_userprofile_properties', ['userprofile_id', 'property_id'])

        # Adding model 'UsersOnline'
        db.create_table('accounts_usersonline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('logged_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('idle', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('accounts', ['UsersOnline'])

        # Adding model 'UserBan'
        db.create_table('accounts_userban', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ban_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ban_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('ban_email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ban_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('reason', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('given_reason', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('accounts', ['UserBan'])


    def backwards(self, orm):
        
        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')

        # Removing M2M table for field properties on 'UserProfile'
        db.delete_table('accounts_userprofile_properties')

        # Deleting model 'UsersOnline'
        db.delete_table('accounts_usersonline')

        # Deleting model 'UserBan'
        db.delete_table('accounts_userban')


    models = {
        'accounts.userban': {
            'Meta': {'object_name': 'UserBan'},
            'ban_email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ban_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'ban_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ban_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'given_reason': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activate_key': ('django.db.models.fields.CharField', [], {'max_length': '127', 'null': 'True', 'blank': 'True'}),
            'activate_key_expirary': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'admin_note': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'banned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'homepage': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'last_ip_used': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'properties': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['util.Property']", 'null': 'True', 'symmetrical': 'False'}),
            'registration_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True'}),
            'remember_between_visits': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'signature': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'New member'", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'accounts.usersonline': {
            'Meta': {'object_name': 'UsersOnline'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idle': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'logged_date': ('django.db.models.fields.DateTimeField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
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
        'util.property': {
            'Meta': {'object_name': 'Property'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'property': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['accounts']
