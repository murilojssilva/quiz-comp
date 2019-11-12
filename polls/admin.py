from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Usuario, Prova, Questao, Categoria, Resposta
from django import forms
from django.urls import reverse
from django.utils.html import escape
from django.utils.html import format_html

admin.site.site_header = "EDUQUIZ"
admin.site.site_title = "Área de administração do EDUQUIZ"
admin.site.index_title = "Área de administração do EDUQUIZ"


class UsuarioInline(admin.StackedInline):
	model = Usuario
	can_delete = False
	verbose_name = 'Informações Pessoais'

class UserAdmin(BaseUserAdmin):
	inlines = (UsuarioInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
	model = Usuario
	list_display = ('user','matricula', 'tipoUsuario' , 'image_tag')

class RespostaAdmin(admin.ModelAdmin):
	model = Resposta
	list_display = ('idQuestao','usuario_', 'resposta','certaresposta')
	def usuario_(self, obj):
		link = reverse("admin:auth_user_change", args=[obj.usuario.id])
		return format_html('<a href="{}">{}</a>', link, obj.usuario.username)
	usuario_.short_description = 'Usuário'


class QuestaoAdmin(admin.ModelAdmin):
	model = Questao
	list_display = ('idQuestao','prova','categorias','tipoQuestao')
	list_display_links = ('idQuestao','prova')
	def prova(self, obj):
		link = reverse("admin:polls_prova_change", args=[obj.idProva.idProva])
		return format_html('<a href="{}">{}</a>', link, obj.idProva.idProva)


class ProvaAdmin(admin.ModelAdmin):
	model = Prova
	list_display = ('idProva','tipoProva','anoProva')

class CategoryChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return "Categoria: {}".format(Categoria.nomeCategoria)

admin.site.register(Prova,ProvaAdmin)

admin.site.register(Questao,QuestaoAdmin)

admin.site.register(Categoria)

admin.site.register(Resposta,RespostaAdmin)