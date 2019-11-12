# -*- coding: utf-8 -*-
import re

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from polls.models import Usuario, Prova, Categoria, Resposta, Questao
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.core.files.images import get_image_dimensions
from django.forms.widgets import ClearableFileInput
from django_select2.forms import ModelSelect2Widget
import json
from django.db.models import BLANK_CHOICE_DASH
from localflavor.br import *


#class QuestaoProvaForm(forms.Form):
    #prova = forms.ModelChoiceField(queryset=Prova.objects.all(),label=u"Prova",widget=ModelSelect2Widget(model=Prova,search_fields=['idProva__icontains'],))
    #questao = forms.ModelChoiceField(queryset=Questao.objects.all(),label=u"Questao",widget=ModelSelect2Widget(model=Questao,search_fields=['idQuestao__icontains'],dependent_fields={'prova': prova}))
    #categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),label=u"Categoria",widget=ModelSelect2Widget(model=Categoria,search_fields=['idCategoria__icontains'],dependent_fields={'prova': prova,'questao':questao}))
    #prova = forms.ModelChoiceField(queryset=Prova.objects.all(),widget=ModelSelect2Widget())
    #questao = forms.ModelChoiceField(queryset=Questao.objects.all(),widget=ModelSelect2Widget())
    #categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),widget=ModelSelect2Widget(dependent_fields={'prova': 'prova', 'questao': 'questao'},))
# Define an inline admin descriptor for Usuario model
# which acts a bit like a singleton

UM = 1
DOIS = 2

STATUS_QUESTAO_CHOICES = (
        (UM,'Ativa'),
        (DOIS,'Inativa'),
    )

class QuestaoProvaForm(forms.Form):
    prova = forms.ChoiceField(choices=BLANK_CHOICE_DASH+[(o.idProva, str(o)) for o in Prova.objects.all()],label='Provas',required=False)
    questao = forms.ModelChoiceField(queryset=Questao.objects.all(),required=False,widget=forms.HiddenInput())
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(),required=False,label="Categorias")
    class Meta:
       fields = ('prova', 'questao', 'categoria')
    def __init__(self, prova=None,categoria=None, *args, **kwargs):
       super().__init__(*args, **kwargs)
       if prova:
         self.fields['questao'].queryset = Questao.objects.filter(idProva=prova)
         if categoria:
           self.fields['categoria'].queryset = Questao.objects.filter(idCategoria=categoria,idProva=prova)

class AprovaForm(forms.ModelForm):
  class Meta:
    model = Questao
    fields = ("statusQuestao",)
    exclude = ("tipoQuestao",) 


class QuestaoForm(forms.ModelForm):
    idQuestao = forms.CharField(max_length=7,label='ID da questão',widget=forms.TextInput(attrs={'placeholder': 'Ex: E200101'}))
    textoQuestao = forms.CharField(max_length=2000,label="Texto da questão")
    perguntaQuestao = forms.CharField(max_length=500,label="Pergunta da questão")
    aOpcao = forms.CharField(max_length=500,label="Letra a")
    bOpcao = forms.CharField(max_length=500,label="Letra b")
    cOpcao= forms.CharField(max_length=500,label="Letra c")
    dOpcao = forms.CharField(max_length=500,label="Letra d")
    eOpcao = forms.CharField(max_length=500,label="Letra e")
    ajuda = forms.CharField(max_length=500,label="Ajuda da questão")
    RESPOSTA_CHOICES = (
       ('A','A'),
       ('B','B'),
       ('C','C'),
       ('D','D'),
       ('E','E'),
    )
    respostaQuestao = forms.CharField(max_length=1,widget=forms.Select(choices=RESPOSTA_CHOICES),label="Resposta da questão")
    STATUS_QUESTAO_CHOICES = (
       (UM,'Ativa'),
       (DOIS,'Inativa'),
    )
    statusQuestao = forms.IntegerField(label='Status da questão',widget=forms.Select(choices=STATUS_QUESTAO_CHOICES),required=True)
    QUESTAO_CHOICES = (
       (UM,'Múltipla escolha'),
       (DOIS,'Discursiva'),
    )
    tipoQuestao = forms.IntegerField(label='Tipo da questão',widget=forms.Select(choices=QUESTAO_CHOICES),required=True)
    class Meta:
       model = Questao
       fields = '__all__' 
    

class UsuarioInline(admin.StackedInline):
    model = Usuario
    can_delete = False
    verbose_name_plural = 'Usuários'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UsuarioInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


ALUNO = 1
PROFESSOR = 2
USUARIO_CHOICES = (
    (ALUNO,'Aluno'),
    (PROFESSOR,'Professor'),
)



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='Primeiro Nome',max_length=30, required=False, help_text='Opcional.')
    last_name = forms.CharField(label='Último Nome',max_length=30, required=False, help_text='Opcional.')
    email = forms.EmailField(label='E-mail',max_length=254, help_text='Informe o seu e-mail (Requerido)')   
    username = forms.CharField(label='Nome de usuário', min_length=4, max_length=150)
    avatar = forms.ImageField(label='Foto de perfil',required=False)
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    idCategoria = forms.ModelMultipleChoiceField(label="Disciplinas",queryset=Categoria.objects.all(),required=False)
    password2 = forms.CharField(label='Confirmação da senha', widget=forms.PasswordInput)
    tipoUsuario = forms.IntegerField(label='Tipo de usuário',widget=forms.Select(choices=USUARIO_CHOICES,attrs={'onchange': 'Hide()'}),required=True)
    matricula = forms.CharField(label='Matrícula',max_length=12,validators=[ validators.RegexValidator(re.compile('^[0-9]{12}$'), _('Digite uma matrícula válida'), _('invalid'))])
    class Meta:
       model = User
       fields = ['first_name', 'last_name','username','email','password1', 'password2','avatar','tipoUsuario','matricula','idCategoria'] 
    def __init__(self, *args, **kwargs):
       # Only in case we build the form from an instance
       # (otherwise, 'idCategoria' list should be empty)
       if kwargs.get('instance'):
         # We get the 'initial' keyword argument or initialize it
         # as a dict if it didn't exist.         
         initial = kwargs.setdefault('initial', {})
         # The widget for a ModelMultipleChoiceField expects
         # a list of primary key for the selected data.
         initial['idCategoria'] = [t.nomeCategoria for t in kwargs['instance'].Categoria_set.all()]

       forms.ModelForm.__init__(self, *args, **kwargs)

    def clean_username(self):
       username = self.cleaned_data['username'].lower()
       r = User.objects.filter(username=username)
       if r.count():
         raise  ValidationError("Nome de usuário já cadastrado")
       return username

    def clean_email(self):
       email = self.cleaned_data['email'].lower()
       r = User.objects.filter(email=email)
       if r.count():
         raise  ValidationError("E-mail já cadastrado")
       return email
       try:
         user = User.objects.get(email=email)
         raise forms.ValidationError("O endereço de e-mail já existe. Você esqueceu sua senha?")
       except User.DoesNotExist:
         return email

    def clean_password2(self):
       password1 = self.cleaned_data.get('password1')
       password2 = self.cleaned_data.get('password2')

       if password1 and password2 and password1 != password2:
         raise ValidationError("Senhas não conferem")

       return password2
    def save(self, commit=True):
       user = User.objects.create_user(
         self.cleaned_data['username'],
         self.cleaned_data['email'],
         self.cleaned_data['password1']
       )
       return user


class LoginForm(forms.Form):
    username = forms.CharField(label = 'Nome de usuário')
    password1 = forms.CharField(label = 'Senha',widget = forms.PasswordInput)
    class Meta:
       model = Usuario
       fields = ('username','password1')

class PontosForm(forms.ModelForm):
    pontos = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
       model = Usuario
       fields = ('pontos',)

class RespostaForm(forms.ModelForm):
    RESPOSTA_CHOICES = (
       ('A','A'),
       ('B','B'),
       ('C','C'),
       ('D','D'),
       ('E','E'),
    )
    usuario = forms.CharField(label='Nome do usuário',widget=forms.HiddenInput())
    idQuestao = forms.CharField(label='ID da questão',widget=forms.HiddenInput())
    resposta = forms.ChoiceField(choices=RESPOSTA_CHOICES, widget=forms.RadioSelect,required=False,)
    A = forms.ChoiceField(widget=forms.RadioSelect,required=False,)
    B = forms.ChoiceField(widget=forms.RadioSelect,required=False,)
    C = forms.ChoiceField(widget=forms.RadioSelect,required=False,)
    D = forms.ChoiceField(widget=forms.RadioSelect,required=False,)
    E = forms.ChoiceField(widget=forms.RadioSelect,required=False,)
    respostaA = forms.CharField(label = 'Resposta da letra A',required=False,widget=forms.Textarea(attrs={"rows":5, "cols":108 ,'style': 'width:100%'}))
    respostaB = forms.CharField(label = 'Resposta da letra B',required=False,widget=forms.Textarea(attrs={"rows":5, "cols":108 ,'style': 'width:100%'}))
    respostaC = forms.CharField(label = 'Resposta da letra C',required=False,widget=forms.Textarea(attrs={"rows":5, "cols":108 ,'style': 'width:100%'}))
    respostaD = forms.CharField(label = 'Resposta da letra D',required=False,widget=forms.Textarea(attrs={"rows":5, "cols":108 ,'style': 'width:100%'}))
    respostaE = forms.CharField(label = 'Resposta da letra E',required=False,widget=forms.Textarea(attrs={"rows":5, "cols":108 ,'style': 'width:100%'}))
    def idQuestao(self):
       pass
    def usuario(self):
       pass
    class Meta:
       model = Resposta
       exclude = ('usuario','idQuestao',)
       fields = ('resposta','respostaA','respostaB','respostaC','respostaD','respostaE','A','B','C','D','E')


class EditProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True,required=False,min_length=4, max_length=150,help_text=("Insira um novo nome de usuário"), label='Nome de usuário')
    first_name = forms.CharField(label='Nome',required=False)
    last_name = forms.CharField(label='Sobrenome',required=False)
    email = forms.EmailField(label='E-mail',required=False)
    matricula = forms.CharField(required=False, disabled=True,label='Matrícula', max_length=12,validators=[ validators.RegexValidator(re.compile('^[0-9]{12}$'), _('Digite uma matrícula válida'), _('invalid'))])
    avatar = forms.ImageField(label='Foto de perfil')
    tipoUsuario = forms.IntegerField(label='Tipo de usuário',widget=forms.Select(choices=USUARIO_CHOICES), disabled=True,required=False)
    idCategoria = forms.ModelMultipleChoiceField(label="Disciplinas",queryset=Categoria.objects.all(),required=False)
    class Meta:
       model = User
       fields = ['username','first_name', 'last_name','email','matricula','avatar','tipoUsuario','idCategoria']
    def clean_avatar(self):
       avatar = self.cleaned_data['avatar']
       try:
         w, h = get_image_dimensions(avatar)
         max_width = max_height = 1000000
         if w > max_width or h > max_height:
          raise forms.ValidationError(
          u'Please use an image that is '
           '%s x %s pixels or smaller.' % (max_width, max_height))
         main, sub = avatar.content_type.split('/')
         if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
          raise forms.ValidationError(u'Please use a JPEG, '
          'GIF or PNG image.')

         #validate file size
         if len(avatar) > (20 * 1024):
          raise forms.ValidationError(
          u'Avatar file size may not exceed 20k.')
       except AttributeError:
         pass

       return avatar

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True,label='Nome de usuário')
    first_name = forms.CharField(label='Nome')
    last_name = forms.CharField(label='Sobrenome')
    email = forms.EmailField(disabled=True,label='E-mail')
    class Meta:
       model = User
       fields = ('username', 'first_name','last_name', 'email' )

class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Atual'
    input_text = 'Alterar'
    clear_checkbox_label = 'Sem fotos'

class UsuarioForm(forms.ModelForm):
    matricula = forms.CharField(disabled=True,label='Matrícula')
    avatar = forms.ImageField(label='Foto de perfil',widget=MyClearableFileInput,required=False)
    tipoUsuario = forms.IntegerField(label='Tipo de usuário',widget=forms.Select(choices=USUARIO_CHOICES),required=True,disabled=True)
    idCategoria = forms.ModelMultipleChoiceField(label="Disciplinas",queryset=Categoria.objects.all(),required=False)
    class Meta:
       model = Usuario
       exclude = ['user']
       fields = ('matricula','avatar','tipoUsuario','idCategoria')

class ProvaForm(forms.ModelForm):
    idProva  = forms.CharField(label='ID da Prova',max_length=5,widget=forms.TextInput(attrs={'placeholder': 'Ex: E2005'}))
    TIPO_PROVA_CHOICES = (
       ('ENADE','ENADE'),
       ('PROFMAT','PROFMAT'),
    )
    tipoProva = forms.CharField(label='Tipo da Prova',widget=forms.Select(choices=TIPO_PROVA_CHOICES))
    anoProva = forms.CharField(label='Ano da Prova',max_length=4)
    class Meta:
       model = Prova
       fields = ('idProva','tipoProva','anoProva')

class CategoriaForm(forms.ModelForm):
    class Meta:
       model = Categoria
       fields = ('idCategoria','nomeCategoria','parent')

    def get_object(self):
       try:
         categoria = Categoria.objects.get(uuid=self.kwargs['uuid'])
         return categoria

       except Categoria.DoesNotExist:
         raise Http404

    def __init__(self, *args, **kwargs):
       super(CategoriaForm, self).__init__(*args, **kwargs)
       self.fields['parent'].choices = categoria_pai_as_choices()
       
def categoria_pai_as_choices():
    categorias = []
    categorias.append(['', '-----------'])
    for categoria in Categoria.objects.filter(parent=None).all():
       categorias.append([categoria.idCategoria, categoria.nomeCategoria])
    return categorias

class CategoriaAdmin(admin.ModelAdmin):
    form = CategoriaForm 


class CategoryChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
       return "Categoria: {}".format(categoria.nomeCategoria)

def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'Categoria':
       return CategoryChoiceField(queryset=Categoria.objects.all())
    return super().formfield_for_foreignkey(db_field, request, **kwargs)

# class OpcaoForm(forms.ModelForm)
#   class Meta:
#   model = Opcao
# class HistoricoForm(forms.ModelForm)
#   class Meta:
#   model = Historico