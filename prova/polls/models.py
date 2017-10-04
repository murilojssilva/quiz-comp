from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import json
from PIL import Image

class Prova(models.Model):
	idProva = models.CharField(max_length=5,primary_key=True,null=False)
	tipoProva = models.CharField(max_length=5,null=False)
	anoProva = models.CharField(max_length=4,null=False)
	def __str__(self):
		return self.idProva

class Usuario(models.Model):
	matriculaUsuario = models.CharField(max_length=12,primary_key=True,null=False)
	nomeUsuario = models.CharField(max_length=200,null=False)
	tipoUsuario = models.CharField(max_length=1,null=False)
	emailUsuario = models.EmailField(null=False)
	senhaUsuario = models.CharField(max_length=20,null=False)
	def __str__(self):
		return self.matriculaUsuario

class Questao(models.Model):
	idQuestao = models.CharField(max_length=7,primary_key=True,null=False)
	idProva = models.ForeignKey(Prova)
	areaQuestao = models.CharField(max_length=50,null=False)
	tipoQuestao = models.CharField(max_length=1,null=False)
	textoQuestao = models.CharField(max_length=2000,blank=True,null=True)
	imagemQuestao = models.FileField(upload_to='static/img/uploads',blank=True,null=True)
	imagem2Questao = models.FileField(upload_to='static/img/uploads',blank=True,null=True)
	perguntaQuestao = models.CharField(max_length=500,blank=True,null=True)
	statusQuestao = models.CharField(max_length=1,null=False)
	def __str__(self):
		return self.idQuestao

class Opcao(models.Model):
	idOpcao = models.CharField(max_length=8,primary_key=True,null=False)
	idQuestao = models.ForeignKey(Questao)
	aOpcao = models.CharField(max_length=500,null=False,blank=True)
	bOpcao = models.CharField(max_length=500,null=False,blank=True)
	cOpcao = models.CharField(max_length=500,null=False,blank=True)
	dOpcao = models.CharField(max_length=500,null=False,blank=True)
	eOpcao = models.CharField(max_length=500,null=False,blank=True)
	escolhidaOpcao = models.CharField(max_length=200,null=True,blank=True)
	def __str__(self):
		return self.idOpcao

class Historico(models.Model):
	idHistorico = models.CharField(max_length=10,primary_key=True,null=False)
	idProva = models.ForeignKey(Prova,null=False)
	matriculaUsuario = models.ForeignKey(Usuario,null=False)
	def __str__(self):
		return self.idHistorico

class Resposta(models.Model):
	idResposta = models.CharField(max_length=9,primary_key=True,null=False)
	idQuestao = models.ForeignKey(Questao)
	resposta = models.CharField(max_length=1,null=False)
	def __str__(self):
		return self.idResposta