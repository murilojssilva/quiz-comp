from django.conf.urls import url
from django.urls import include, path

import django.contrib.auth.views

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout_then_login
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django_filters.views import FilterView
from .filters import FiltroQuestoes
from rest_framework import routers
from .views import QuestaoViewset, ProvaViewset,ProvaQuestaoViewset


router = routers.DefaultRouter()
router.register(r'questao',QuestaoViewset)
router.register(r'prova',ProvaViewset)

from django.conf.urls import (handler400, handler403, handler404, handler500)

handler400 = 'polls.views.bad_request'
handler403 = 'polls.views.permission_denied'
handler404 = 'polls.views.page_not_found'
handler500 = 'polls.views.server_error'


urlpatterns = [
	url(r'^registrar/$', views.registrar, name='registrar'),
	url(r'^api/',include(router.urls)),
	#url('^', include('django.contrib.auth.urls')),
	url(r'^select2/', include('django_select2.urls')),
	url(r'^test',views.get_data,name="getdata"),
	url(r'^$', views.index,name='index'),
	url(r'^registrar/$', views.registrar,name='registrar'),
	#url(r'^quiz/$', views.quiz,name='quiz'),
	path('quiz/', views.quiz, name='quiz'),
	url(r'^quiz/selecionar$', views.seletor_quiz,name='seletor_quiz'),
	url(r'^login/$', LoginView.as_view(template_name='polls/login.html'), name="login"),
	url(r'^logout/$', logout_then_login,{'login_url': '/login/'},name='logout'),
	url(r'^alterarsenha/$', views.alterarsenha, name='alterarsenha'),
	url(r'^perfil/$', views.profile_view, name='profile'),
	url(r'^perfil/editarperfil/$', views.edit_profile, name='edit_profile'),
	path('filter_dropdown2/', views.filter_dropdown2, name='filter_dropdown2'),
	path('questoes/ajax/', views.questoes_ajax, name='questoes_ajax'),
	path('questoes/choices/ajax/',views.questoes_choices_ajax,name='questoes_choices_ajax'),
	url(r'^questoes/nova/',views.add_questoes,name="add_questoes"),
	url(r'^questoes/lista_aprovacao/',views.lista_aprovacao,name="lista_aprovacao"),
	url(r'^provas/nova/',views.add_provas,name="add_provas"),
	path('categorias/ajax/', views.categorias_ajax, name='categorias_ajax'),
	path('categorias/choices/ajax/',views.categorias_choices_ajax,name='categorias_choices_ajax'),
	url(r'^categorias/nova/',views.add_categorias,name="add_categorias"),
	url(r'^pesquisa/$', views.pesquisa),
	url(r'^desempenho/$', views.desempenho,name='desempenho'),
	url(r'^desempenho_alunos/$', views.desempenho_disciplinas,name='desempenho_disciplinas'),
	#url(r'^thanks/$', views.thanks,name='thanks'),
	#url(r'^(?P<idProva>[-_\w]+)/(?P<idQuestao>[-_\w]+)/resposta/$', views.resposta, name='resposta'),
	url('<int:pk>/resultado/', views.resultado, name='resultado'),
	#url(r'^(?P<idCategoria>[-_\w]+)/$', views.categoria, name='categoria'),
	url(r'^(?P<idProva>[-_\w]+)/(?P<idQuestao>\w+)/$', views.questoes,name="questoes"),
	url(r'^(?P<idProva>[-_\w]+)/$', views.detalhes,name='detalhes'),
	#path('lista_de_questoes/', views.lista_de_questoes, name='lista_de_questoes'),
	#path('ajax/load-questoes/', views.load_questoes, name='ajax_load_questoes'),
	#path('ajax/load-categorias/', views.load_categorias, name='ajax_load_categorias'),
	#url(r'^(?P<idProva>\w+)/$', views.resultados, name ='resultados'),
	#url(r'^(?P<idProva>\w+)/resultados/$', views.resultados, name='resultados'),
	#url(r'^(?P<idProva>\w+)/(?P<idQuestao>\w+)$', views.resposta, name='resposta'),
	#url(r'^(?P<idProva>\w+)/(?P<idQuestao>\w+)/(?P<idOpcao>\w+)/$', views.detalhes, name ='detalhes'),
	#url(r'^(?P<idProva>\w+)/$', views.detalhes, name='resposta'),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)