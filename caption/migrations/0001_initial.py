# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 00:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_creator', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('played', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SlugField(max_length=5, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('flag', models.ImageField(blank=True, null=True, upload_to='flags')),
            ],
            options={
                'ordering': ['code'],
            },
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField()),
                ('text', models.CharField(max_length=400)),
                ('cue_in', models.IntegerField(blank=True, null=True)),
                ('cue_out', models.IntegerField(blank=True, null=True)),
                ('stanza', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['item', 'number'],
            },
        ),
        migrations.CreateModel(
            name='Linetrans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=400)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linetrans_creator', to=settings.AUTH_USER_MODEL)),
                ('line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caption.Line')),
            ],
            options={
                'ordering': ['line'],
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caption.Language')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=200)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['item', 'language'],
            },
        ),
        migrations.CreateModel(
            name='Youtube',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='caption.Item')),
                ('key', models.CharField(max_length=11, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('caption.item',),
        ),
        migrations.AddField(
            model_name='translation',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caption.Item'),
        ),
        migrations.AddField(
            model_name='translation',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caption.Language'),
        ),
        migrations.AddField(
            model_name='translation',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translation_updater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='items',
            field=models.ManyToManyField(blank=True, to='caption.Item'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='member',
            name='likes',
            field=models.ManyToManyField(blank=True, to='caption.Item'),
        ),
        migrations.AddField(
            model_name='member',
            name='subscriptions',
            field=models.ManyToManyField(blank=True, to='caption.Playlist'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='linetrans',
            name='translation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caption.Translation'),
        ),
        migrations.AddField(
            model_name='linetrans',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='linetrans_updater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='line',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caption.Item'),
        ),
        migrations.AddField(
            model_name='line',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_updater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='artists',
            field=models.ManyToManyField(blank=True, to='caption.Artist'),
        ),
        migrations.AddField(
            model_name='item',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='caption.Language'),
        ),
        migrations.AddField(
            model_name='item',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_updater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='translation',
            unique_together=set([('item', 'language')]),
        ),
        migrations.AlterUniqueTogether(
            name='line',
            unique_together=set([('item', 'number')]),
        ),
    ]
