# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from polls.models import Prova, Usuario, Questao, Opcao, Resposta, Historico, Categoria

class CategoriaForm(forms.ModelForm):
	idCategoria = forms.CharField(label='Id da Prova',max_length=5)
	nomeCategoria = forms.CharField(label='Categoria',max_length=20)
	class Meta:
 		model = Categoria
 		fields = ('idCategoria','nomeCategoria')

class ProvaForm(forms.ModelForm):
	idProva  = forms.CharField(label='Id da Prova',max_length=5)
	tipoProva = forms.CharField(label='Tipo da Prova',max_length=5)
	anoProva = forms.CharField(label='Ano da Prova',max_length=4)
 	class Meta:
 		model = Prova
 		fields = ('idProva','tipoProva','anoProva')

class UsuarioForm(UserCreationForm):
	matriculaUsuario = forms.CharField(label='Matrícula do Usuário',max_length=12)
	tipoUsuario = forms.CharField(label='1 - Aluno 2 - Professor',max_length=1)
	class Meta:
		model = User
		fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2', )



class LoginForm(forms.Form):
	matriculaUsuario = forms.CharField(label = 'Nombre de usuario')
	senhaUsuario = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput)
	class Meta:
		model = Usuario
		fields = ('matriculaUsuario','senhaUsuario')

class AlterarSenhaForm(forms.ModelForm):
	class Meta:
		model = Usuario
		widgets = {
			'senhaUsuario': forms.PasswordInput(),
		}
		fields = ('matriculaUsuario','senhaUsuario','senhaUsuario')


# class QuestaoForm(forms.ModelForm)
# 	textoQuestao = forms.CharField(label='Texto da questão')
# 	imagemQuestao = forms.ImageField()
# 	perguntaQuestao = forms.CharField(label='Pergunta da questão',null=False)
# 	class Meta:
# 		model = Questao

# class OpcaoForm(forms.ModelForm)
# 	class Meta:
# 		model = Opcao

# class RespostaForm(forms.ModelForm)
	
# 	class Meta:
# 		model = Resposta

# class HistoricoForm(forms.ModelForm)
# 	class Meta:
# 		model = Historico