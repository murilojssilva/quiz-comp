from django.conf.urls import url
import django.contrib.auth.views

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout_then_login
from django.contrib.auth import views as auth_views



urlpatterns = [
	#url(r'^registrar/$', views.registrar, name='registrar'),
	url(r'^$', views.index, name='index'),
	url(r'^registrar/$', views.registrar,name='registrar'),
	url(r'^login/$', LoginView.as_view(template_name='polls/login.html'), name="login"),
	url(r'^logout/$', logout_then_login,{'login_url': '/login/'},name='logout'),
	url(r'^alterarsenha/$', views.alterarsenha, name='alterarsenha'),
	url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
	url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
	url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

	url(r'^thanks/$', views.thanks,name='thanks'),

	url(r'^(?P<idProva>[-_\w]+)/(?P<idQuestao>[-_\w]+)/resposta/$', views.resposta, name='resposta'),
	url(r'^(?P<idProva>[-_\w]+)/(?P<idQuestao>[-_\w]+)/$', views.questoes, name='questoes'),
	url(r'^(?P<idProva>[-_\w]+)/$', views.detalhes),



	#url(r'^(?P<idProva>\w+)/$', views.resultados, name ='resultados'),
	#url(r'^(?P<idProva>\w+)/resultados/$', views.resultados, name='resultados'),
	#url(r'^(?P<idProva>\w+)/(?P<idQuestao>\w+)$', views.resposta, name='resposta'),
	#url(r'^(?P<idProva>\w+)/(?P<idQuestao>\w+)/(?P<idOpcao>\w+)/$', views.detalhes, name ='detalhes'),
	#url(r'^(?P<idProva>\w+)/$', views.detalhes, name='resposta'),
]
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)