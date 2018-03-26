# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-02-22 17:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='about',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='chatgroup',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='is_member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='topic',
            name='arrow_downs',
            field=models.ManyToManyField(blank=True, related_name='arrow_downs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='topic',
            name='arrow_ups',
            field=models.ManyToManyField(blank=True, related_name='arrow_ups', to=settings.AUTH_USER_MODEL),
        ),
    ]