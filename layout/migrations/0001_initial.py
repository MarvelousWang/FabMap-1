# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-25 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EQLayout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eq_name', models.CharField(default='', max_length=50, verbose_name='昵称')),
                ('floor', models.CharField(choices=[('L10', 'L10'), ('L20', 'L20'), ('L30', 'L30'), ('L40', 'L40')], default='楼层未选', max_length=10, verbose_name='楼层')),
                ('vertex', models.CharField(max_length=100, verbose_name='顶点坐标')),
            ],
            options={
                'verbose_name': '机台外框图',
                'verbose_name_plural': '机台外框图',
            },
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor', models.CharField(choices=[('L10', 'L10'), ('L20', 'L20'), ('L30', 'L30'), ('L40', 'L40')], default='楼层未选', max_length=10, verbose_name='楼层')),
                ('path_node', models.CharField(max_length=200, verbose_name='路径节点坐标')),
            ],
            options={
                'verbose_name': '路径图',
                'verbose_name_plural': '路径图',
            },
        ),
    ]
