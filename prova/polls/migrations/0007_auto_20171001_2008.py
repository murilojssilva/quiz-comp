# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20171001_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opcao',
            name='aOpcao',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='opcao',
            name='bOpcao',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='opcao',
            name='cOpcao',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='opcao',
            name='dOpcao',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='opcao',
            name='eOpcao',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]