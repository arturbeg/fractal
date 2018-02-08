# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-01-26 18:24
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
            name='ChatGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('about', models.CharField(max_length=200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('avatar', models.ImageField(blank=True, upload_to='group_avatar')),
                ('label', models.SlugField(unique=True)),
                ('members', models.ManyToManyField(related_name='is_member', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.SlugField(unique=True)),
                ('chatgroup', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chats.ChatGroup')),
                ('current_participants', models.ManyToManyField(related_name='globalchat_current', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LocalChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('about', models.CharField(max_length=200)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_private', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, upload_to='local_chat_avatar')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('label', models.SlugField(unique=True)),
                ('chatgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.ChatGroup')),
                ('current_participants', models.ManyToManyField(related_name='localchat_current', to=settings.AUTH_USER_MODEL)),
                ('participants', models.ManyToManyField(related_name='is_participant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.CharField(blank=True, max_length=200)),
                ('avatar', models.ImageField(blank=True, upload_to='profile_avatar')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='is_following', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('about', models.CharField(max_length=200)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_private', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, upload_to='topic_avatar')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('label', models.SlugField(unique=True)),
                ('arrow_downs', models.ManyToManyField(related_name='arrow_downs', to=settings.AUTH_USER_MODEL)),
                ('arrow_ups', models.ManyToManyField(related_name='arrow_ups', to=settings.AUTH_USER_MODEL)),
                ('chatgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.ChatGroup')),
                ('current_participants', models.ManyToManyField(related_name='topic_current', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]