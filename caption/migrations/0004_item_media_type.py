# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caption', '0003_auto_20170214_0155'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='media_type',
            field=models.CharField(choices=[('ytb', 'youtube'), ('mp3', 'mp3')], default='ytb', max_length=3),
        ),
    ]
