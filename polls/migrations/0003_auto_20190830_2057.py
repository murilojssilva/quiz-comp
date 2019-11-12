# Generated by Django 2.2.4 on 2019-08-30 20:57

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20190819_1729'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resposta',
            name='respostaF',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='avatar',
            field=models.ImageField(default='static/img/user.jpg', upload_to='static/img/uploads/profile_photo', verbose_name='Foto de perfil'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='matricula',
            field=models.CharField(help_text='São requeridos os 12 dígitos referentes à sua matrícula da UERJ', max_length=12, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[0-9]{12}$'), 'Digite uma matrícula válida', 'invalid')], verbose_name='Matrícula'),
        ),
    ]