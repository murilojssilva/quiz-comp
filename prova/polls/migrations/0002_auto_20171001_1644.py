# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questao',
            name='imagemQuestao',
            field=models.ImageField(blank=True, null=True, upload_to='polls'),
        ),
        migrations.AlterField(
            model_name='questao',
            name='textoQuestao',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
