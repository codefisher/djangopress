# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Property'
        db.create_table('util_property', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('class_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('property', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('util', ['Property'])

        # Adding model 'CharProperty'
        db.create_table('util_charproperty', (
            ('property_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['util.Property'], unique=True, primary_key=True)),
            ('property_value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('util', ['CharProperty'])

        # Adding model 'IntProperty'
        db.create_table('util_intproperty', (
            ('property_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['util.Property'], unique=True, primary_key=True)),
            ('property_value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('util', ['IntProperty'])


    def backwards(self, orm):
        
        # Deleting model 'Property'
        db.delete_table('util_property')

        # Deleting model 'CharProperty'
        db.delete_table('util_charproperty')

        # Deleting model 'IntProperty'
        db.delete_table('util_intproperty')


    models = {
        'util.charproperty': {
            'Meta': {'object_name': 'CharProperty', '_ormbases': ['util.Property']},
            'property_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['util.Property']", 'unique': 'True', 'primary_key': 'True'}),
            'property_value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'util.intproperty': {
            'Meta': {'object_name': 'IntProperty', '_ormbases': ['util.Property']},
            'property_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['util.Property']", 'unique': 'True', 'primary_key': 'True'}),
            'property_value': ('django.db.models.fields.IntegerField', [], {})
        },
        'util.property': {
            'Meta': {'object_name': 'Property'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'property': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['util']
