# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('blog_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=50, blank=True)),
        ))
        db.send_create_signal('blog', ['Tag'])

        # Adding model 'Category'
        db.create_table('blog_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=50, blank=True)),
            ('parent_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Category'], null=True, blank=True)),
        ))
        db.send_create_signal('blog', ['Category'])

        # Adding model 'Blog'
        db.create_table('blog_blog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, unique=True, null=True, blank=True)),
            ('tagline', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('blog', ['Blog'])

        # Adding model 'Entry'
        db.create_table('blog_entry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Blog'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('edited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='DR', max_length=2)),
            ('sticky', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visibility', self.gf('django.db.models.fields.CharField')(default='VI', max_length=2)),
        ))
        db.send_create_signal('blog', ['Entry'])

        # Adding M2M table for field tags on 'Entry'
        db.create_table('blog_entry_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['blog.entry'], null=False)),
            ('tag', models.ForeignKey(orm['blog.tag'], null=False))
        ))
        db.create_unique('blog_entry_tags', ['entry_id', 'tag_id'])

        # Adding M2M table for field categories on 'Entry'
        db.create_table('blog_entry_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entry', models.ForeignKey(orm['blog.entry'], null=False)),
            ('category', models.ForeignKey(orm['blog.category'], null=False))
        ))
        db.create_unique('blog_entry_categories', ['entry_id', 'category_id'])

        # Adding model 'EntryMenuLink'
        db.create_table('blog_entrymenulink', (
            ('menulink_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['menus.MenuLink'], unique=True, primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Entry'])),
        ))
        db.send_create_signal('blog', ['EntryMenuLink'])


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('blog_tag')

        # Deleting model 'Category'
        db.delete_table('blog_category')

        # Deleting model 'Blog'
        db.delete_table('blog_blog')

        # Deleting model 'Entry'
        db.delete_table('blog_entry')

        # Removing M2M table for field tags on 'Entry'
        db.delete_table('blog_entry_tags')

        # Removing M2M table for field categories on 'Entry'
        db.delete_table('blog_entry_categories')

        # Deleting model 'EntryMenuLink'
        db.delete_table('blog_entrymenulink')


    models = {
        'blog.blog': {
            'Meta': {'object_name': 'Blog'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'blog.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'parent_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'blog.entry': {
            'Meta': {'object_name': 'Entry'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Blog']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Category']", 'symmetrical': 'False'}),
            'edited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'DR'", 'max_length': '2'}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visibility': ('django.db.models.fields.CharField', [], {'default': "'VI'", 'max_length': '2'})
        },
        'blog.entrymenulink': {
            'Meta': {'object_name': 'EntryMenuLink', '_ormbases': ['menus.MenuLink']},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.Entry']"}),
            'menulink_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['menus.MenuLink']", 'unique': 'True', 'primary_key': 'True'})
        },
        'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'menus.menulink': {
            'Meta': {'object_name': 'MenuLink'},
            'class_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['blog']
