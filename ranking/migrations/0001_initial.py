# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stock'
        db.create_table(u'ranking_stock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exchange', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('symbol', self.gf('django.db.models.fields.CharField')(unique=True, max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'ranking', ['Stock'])


    def backwards(self, orm):
        # Deleting model 'Stock'
        db.delete_table(u'ranking_stock')


    models = {
        u'ranking.stock': {
            'Meta': {'object_name': 'Stock'},
            'exchange': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'symbol': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        }
    }

    complete_apps = ['ranking']