# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='status',
            field=models.CharField(default=-1, max_length=2, choices=[(-1, b'Unconfirmed Email'), (0, b'New User'), (1, b'Full Access')]),
            preserve_default=True,
        ),
    ]
