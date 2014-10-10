# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20141006_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='performance',
            new_name='stock_performance',
        ),
        migrations.AddField(
            model_name='post',
            name='log_votes',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='post_performance',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='votes',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
