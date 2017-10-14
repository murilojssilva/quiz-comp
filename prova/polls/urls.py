from django.conf.urls import url
import django.contrib.auth.views

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	#url(r'^registrar/$', views.registrar, name='registrar'),
	url(r'^$', views.index, name='index'),
	url(r'^registrar/$', views.registrar,name='registrar'),
	url(r'^login/$', views.user_login,name='login'),
	url(r'^logout/$', views.logout,name='logout'),
	url(r'^alterarsenha/$', views.alterarsenha,name='alterarsenha'),
	url(r'^thanks/$', views.thanks,name='thanks'),
	url(r'^(?P<idProva>\w+)/$', views.detalhes, name ='detalhes'),
	#url(r'^(?P<idProva>\w+)/$', views.resultados, name ='resultados'),
	#url(r'^(?P<idProva>\w+)/resultados/$', views.resultados, name='resultados'),
	url(r'^(?P<idProva>\w+)/(?P<idQuestao>\w+)/resposta/$', views.resposta, name='resposta'),
	#url(r'^(?P<idProva>\w+)/(?P<idQuestao>\w+)/(?P<idOpcao>\w+)/$', views.detalhes, name ='detalhes'),
	#url(r'^(?P<idProva>\w+)/$', views.detalhes, name='resposta'),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)