# Generated by Django 2.2.5 on 2019-10-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20191028_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='idCategoria',
            field=models.ManyToManyField(blank=True, default='', to='polls.Categoria', verbose_name='Disciplina'),
        ),
    ]