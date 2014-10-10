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
            field=models.CharField(default=b'E', max_length=2, choices=[(b'E', b'Unconfirmed Email'), (b'N', b'New User'), (b'F', b'Full Access')]),
            preserve_default=True,
        ),
    ]
