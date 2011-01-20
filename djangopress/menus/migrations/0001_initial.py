# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MenuLink'
        db.create_table('menus_menulink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('menus', ['MenuLink'])

        # Adding model 'Menu'
        db.create_table('menus_menu', (
            ('parent_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menus.MenuItem'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
        ))
        db.send_create_signal('menus', ['Menu'])

        # Adding model 'MenuItem'
        db.create_table('menus_menuitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menus.Menu'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menus.MenuLink'])),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('menus', ['MenuItem'])

        # Adding model 'StaticLink'
        db.create_table('menus_staticlink', (
            ('menulink_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['menus.MenuLink'], unique=True, primary_key=True)),
            ('location', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('menus', ['StaticLink'])


    def backwards(self, orm):
        
        # Deleting model 'MenuLink'
        db.delete_table('menus_menulink')

        # Deleting model 'Menu'
        db.delete_table('menus_menu')

        # Deleting model 'MenuItem'
        db.delete_table('menus_menuitem')

        # Deleting model 'StaticLink'
        db.delete_table('menus_staticlink')


    models = {
        'menus.menu': {
            'Meta': {'object_name': 'Menu'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'parent_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menus.MenuItem']", 'null': 'True', 'blank': 'True'})
        },
        'menus.menuitem': {
            'Meta': {'object_name': 'MenuItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menus.MenuLink']"}),
            'parent_menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menus.Menu']"}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'menus.menulink': {
            'Meta': {'object_name': 'MenuLink'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'menus.staticlink': {
            'Meta': {'object_name': 'StaticLink', '_ormbases': ['menus.MenuLink']},
            'location': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'menulink_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['menus.MenuLink']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['menus']
