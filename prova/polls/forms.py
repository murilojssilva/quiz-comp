# -*- coding: utf-8 -*-
from django import forms
from polls.models import Prova, Usuario, Questao, Opcao, Resposta, Historico

class ProvaForm(forms.ModelForm):
	idProva  = forms.CharField(label='Id da Prova',max_length=5)
	tipoProva = forms.CharField(label='Tipo da Prova',max_length=5)
	anoProva = forms.CharField(label='Ano da Prova',max_length=4)
 	class Meta:
 		model = Prova
 		fields = ('idProva','tipoProva','anoProva')

class UsuarioForm(forms.ModelForm):
	matriculaUsuario = forms.CharField(label='Matrícula do Usuário',max_length=12)
	nomeUsuario = forms.CharField(label='Nome do Usuário',max_length=200)
	emailUsuario = forms.EmailField(label='E-mail')
	tipoUsuario = forms.CharField(label='1 - Aluno 2 - Professor',max_length=1)
	senhaUsuario = forms.CharField(max_length=20)
	fotoUsuario = forms.FileField(label='Foto do avatar')
	class Meta:
		model = Usuario
		widgets = {
			'senhaUsuario': forms.PasswordInput(),
		}
		fields = ('matriculaUsuario','nomeUsuario','emailUsuario','tipoUsuario','senhaUsuario','fotoUsuario')



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