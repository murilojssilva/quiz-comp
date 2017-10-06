from django.conf.urls import url

from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	#url(r'^registrar/$', views.registrar, name='registrar'),
	url(r'^$', views.index, name='index'),
	url(r'^registrar/$', views.registrar,name='registrar'),
	url(r'^login/$', views.user_login,name='login'),
	url(r'^(?P<idProva>\w+)/$', views.detalhes, name ='detalhes'),
	#url(r'^(?P<idProva>\w+)/$', views.resultados, name ='resultados'),
	url(r'^(?P<idProva>\w+)/resultados/$', views.resultados, name='resultados'),
	url(r'^(?P<idProva>\w+)/resposta/$', views.resposta, name='resposta'),
	
	#url(r'^(?P<idProva>\w+)/(?P<idQuestao>\w+)/$', views.detalhes, name ='detalhes'),
	#url(r'^(?P<idProva>\w+)/(?P<idQuestao>\w+)/(?P<idOpcao>\w+)/$', views.detalhes, name ='detalhes'),
	#url(r'^(?P<idProva>\w+)/$', views.detalhes, name='resposta'),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)