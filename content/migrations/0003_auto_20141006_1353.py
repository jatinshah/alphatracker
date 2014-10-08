# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_auto_20140930_0837'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='performance',
            field=models.FloatField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='performance_updated_on',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
