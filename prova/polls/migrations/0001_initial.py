# Generated by Django 2.1.5 on 2019-04-18 01:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('idCategoria', models.CharField(default='Categoria', max_length=12, primary_key=True, serialize=False)),
                ('nomeCategoria', models.CharField(max_length=30)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materias', to='polls.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Prova',
            fields=[
                ('idProva', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('tipoProva', models.CharField(max_length=5)),
                ('anoProva', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Questao',
            fields=[
                ('idQuestao', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('textoQuestao', models.CharField(blank=True, max_length=2000, null=True)),
                ('imagemQuestao', models.FileField(blank=True, null=True, upload_to='static/img/uploads')),
                ('imagem2Questao', models.FileField(blank=True, null=True, upload_to='static/img/uploads')),
                ('perguntaQuestao', models.CharField(blank=True, max_length=500, null=True)),
                ('aOpcao', models.CharField(blank=True, max_length=500)),
                ('bOpcao', models.CharField(blank=True, max_length=500)),
                ('cOpcao', models.CharField(blank=True, max_length=500)),
                ('dOpcao', models.CharField(blank=True, max_length=500)),
                ('eOpcao', models.CharField(blank=True, max_length=500)),
                ('respostaQuestao', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1)),
                ('statusQuestao', models.IntegerField(choices=[(1, 'Ativa'), (2, 'Inativa')], verbose_name='Status de questão')),
                ('tipoQuestao', models.IntegerField(choices=[(1, 'Múltipla escolha'), (2, 'Discursiva')], verbose_name='Tipo de questão')),
                ('idCategoria', models.ManyToManyField(default='Categorias', to='polls.Categoria')),
                ('idProva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Prova')),
            ],
        ),
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resposta', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], max_length=1)),
                ('certaresposta', models.BooleanField(default=True)),
                ('idQuestao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Questao')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(help_text='São requeridos os 12 dígitos referentes à sua matrícula da UERJ', max_length=12, validators=[django.core.validators.RegexValidator(re.compile('^[0-9]{12}$'), 'Digite uma matrícula válida', 'invalid')], verbose_name='Matrícula')),
                ('avatar', models.ImageField(blank=True, default='static/img/user.jpg', upload_to='static/img/uploads/profile_photo', verbose_name='Foto de perfil')),
                ('tipoUsuario', models.IntegerField(choices=[(1, 'Aluno'), (2, 'Professor')], default=1, verbose_name='Tipo de Usuário')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
