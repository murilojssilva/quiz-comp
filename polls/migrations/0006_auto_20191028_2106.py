# Generated by Django 2.2.5 on 2019-10-28 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_questao_ajuda'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='idCategoria',
            field=models.ManyToManyField(default='Disciplinas', to='polls.Categoria', verbose_name='Disciplina'),
        ),
        migrations.AlterField(
            model_name='questao',
            name='idCategoria',
            field=models.ManyToManyField(default='Categorias', to='polls.Categoria', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='questao',
            name='idProva',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Prova', verbose_name='Prova'),
        ),
    ]