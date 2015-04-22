# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nmatch', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='preferences',
            old_name='prefer',
            new_name='a1',
        ),
        migrations.AddField(
            model_name='preferences',
            name='a2',
            field=models.IntegerField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preferences',
            name='a3',
            field=models.SlugField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preferences',
            name='a4',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preferences',
            name='a5',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='preferences',
            name='a6',
            field=models.IntegerField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
