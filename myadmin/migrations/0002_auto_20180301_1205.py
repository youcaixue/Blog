# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-01 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='count',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='article',
            name='sort',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
