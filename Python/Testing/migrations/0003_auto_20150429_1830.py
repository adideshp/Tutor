# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Testing', '0002_auto_20150429_1829'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test_summary',
            old_name='time_taken',
            new_name='total_time',
        ),
    ]
