# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Testing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test_summary',
            name='total_time',
        ),
        migrations.AddField(
            model_name='test_summary',
            name='time_taken',
            field=models.IntegerField(default=0),
        ),
    ]
