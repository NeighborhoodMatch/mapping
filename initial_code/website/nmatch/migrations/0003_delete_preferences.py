# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nmatch', '0002_auto_20150306_2309'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Preferences',
        ),
    ]
