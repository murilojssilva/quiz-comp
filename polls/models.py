import re

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import json
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core import validators
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.db.models import Q

UM = 1
DOIS = 2		

class Prova(models.Model):
	idProva = models.CharField(max_length=5,primary_key=True,null=False,verbose_name="ID da prova")
	TIPO_PROVA_CHOICES = (
       ('ENADE','ENADE'),
       ('PROFMAT','PROFMAT'),
    )
	tipoProva = models.CharField(max_length=7,choices=TIPO_PROVA_CHOICES,null=False,verbose_name="Tipo da prova")
	anoProva = models.CharField(max_length=4,null=False,verbose_name="Ano da prova")
	def __str__(self):
		return self.idProva
		verbose_name_plural = "Provas"

class Categoria(models.Model):
	idCategoria = models.CharField(primary_key=True,max_length=12,null=False,default='Categoria',verbose_name="ID da Categoria")
	nomeCategoria = models.CharField(max_length=30,null=False,verbose_name="Categoria")
	parent = models.ForeignKey('self',blank=True, null=True ,related_name='materias', on_delete=models.CASCADE)
	def __str__(self):
		return self.nomeCategoria
		verbose_name_plural = "Categorias"
	@property
	def get_categoria(self):
		return Questao.objects.filter(categoria__idCategoria=self.idCategoria)

class Questao(models.Model):
	idQuestao = models.CharField(max_length=7,primary_key=True,null=False,verbose_name="ID da questão")
	idProva = models.ForeignKey(Prova,on_delete=models.CASCADE,verbose_name="Prova")
	idCategoria = models.ManyToManyField(Categoria,default="Categorias",verbose_name="Categoria")
	textoQuestao = models.CharField(max_length=2000,blank=True,null=True,verbose_name="Texto da questão")
	imagemQuestao = models.FileField(upload_to='static/img/uploads',blank=True,null=True,verbose_name="Imagem da questão")
	imagem2Questao = models.FileField(upload_to='static/img/uploads',blank=True,null=True,verbose_name="Imagem 2 da questão")
	perguntaQuestao = models.CharField(max_length=500,blank=True,null=True,verbose_name="Pergunta da questão")
	aOpcao = models.CharField(max_length=500,null=False,blank=True,verbose_name="Letra a")
	bOpcao = models.CharField(max_length=500,null=False,blank=True,verbose_name="Letra b")
	cOpcao = models.CharField(max_length=500,null=False,blank=True,verbose_name="Letra c")
	dOpcao = models.CharField(max_length=500,null=False,blank=True,verbose_name="Letra d")
	eOpcao = models.CharField(max_length=500,null=False,blank=True,verbose_name="Letra e")
	ajuda = models.CharField(max_length=500,verbose_name="Ajuda da questão",null=True,default="",blank=True)
	RESPOSTA_CHOICES = (
		('A','A'),
		('B','B'),
		('C','C'),
		('D','D'),
		('E','E'),
	)
	respostaQuestao = models.CharField(max_length=1,choices=RESPOSTA_CHOICES,verbose_name="Resposta da questão")
	STATUS_QUESTAO_CHOICES = (
		(UM,'Ativa'),
		(DOIS,'Inativa'),
	)
	statusQuestao = models.IntegerField('Status de questão',choices=STATUS_QUESTAO_CHOICES,null=False)
	QUESTAO_CHOICES = (
		(UM,'Múltipla escolha'),
		(DOIS,'Discursiva'),
	)
	tipoQuestao = models.IntegerField('Tipo de questão',choices=QUESTAO_CHOICES,null=False)
	def categorias(self):
		return "\n".join([p.nomeCategoria for p in self.idCategoria.all()])
	def __str__(self):
		return self.idQuestao
	def __unicode__(self):
		return self.idQuestao
	class Meta:
		verbose_name = "Questão"
		verbose_name_plural = "Questões"

class Resposta(models.Model):
	idQuestao = models.ForeignKey(Questao,on_delete=models.CASCADE,verbose_name="ID da questão")
	usuario = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Usuário")
	RESPOSTA_CHOICES = (
		('A','A'),
		('B','B'),
		('C','C'),
		('D','D'),
		('E','E'),
	)
	resposta = models.CharField(max_length=1,choices=RESPOSTA_CHOICES,verbose_name="Resposta")
	respostaA = models.CharField(max_length=2000,blank=True,null=True,verbose_name="Resposta da letra a")
	respostaB = models.CharField(max_length=2000,blank=True,null=True,verbose_name="Resposta da letra b")
	respostaC = models.CharField(max_length=2000,blank=True,null=True,verbose_name="Resposta da letra c")
	respostaD = models.CharField(max_length=2000,blank=True,null=True,verbose_name="Resposta da letra d")
	respostaE = models.CharField(max_length=2000,blank=True,null=True,verbose_name="Resposta da letra e")
	certaresposta = models.BooleanField(default=False)
	def __str__(self):
		return self.resposta
	def get_respostas(self):
		return self.resposta_set.filter(usuario=request.user)
	class Meta:
		verbose_name = "Resposta"
		verbose_name_plural = "Respostas"

class Usuario(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE,verbose_name="Usuário")
	matricula = models.CharField('Matrícula',max_length=12,unique=True,null=False,help_text=_('São requeridos os 12 dígitos referentes à sua matrícula da UERJ'), validators=[ validators.RegexValidator(re.compile('^[0-9]{12}$'), _('Digite uma matrícula válida'), _('invalid'))])
	avatar = models.ImageField('Foto de perfil',upload_to='static/img/uploads/profile_photo',default="static/img/user.jpg")
	pontos = models.IntegerField(verbose_name="Pontuação",default=0)
	idCategoria = models.ManyToManyField(Categoria,default="Categorias",verbose_name="Categoria") 
	USUARIO_CHOICES = (
		(UM,'Aluno'),
		(DOIS,'Professor'),
	)
	tipoUsuario = models.IntegerField('Tipo de Usuário',choices=USUARIO_CHOICES,default=1)
	class Meta:
		verbose_name = "Usuário"
		verbose_name_plural = "Usuários"
	def image_tag(self):
		if self.avatar:
			return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.avatar.url)
		else:
			return 'Sem imagem'
	image_tag.short_description = 'Imagem'
	def thumbnail(self):
		return render_to_string('polls/edit_profile.html', {'image': self})
@receiver(post_save, sender=User)
def update_user_usuario(sender, instance, created, **kwargs):
	if created:
		Usuario.objects.create(user=instance)
	instance.usuario.save()
@receiver(post_save, sender=User)
def update_user_usuario(sender, instance, created, **kwargs):
	if created:
		Usuario.objects.create(user=instance)
	instance.usuario.save()