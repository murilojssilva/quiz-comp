# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Usuario,Prova, Questao, Categoria, Resposta
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, logout, authenticate
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.db.models import Q
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
import json
from itertools import chain
from .filters import FiltroQuestoes
import json as simplejson
from django.db import models
from django.shortcuts import (render_to_response)
from django.template import RequestContext
from rest_framework import viewsets
from .serializer import QuestaoSerialzer, ProvaSerializer
from quiz.settings import EMAIL_HOST_USER
from django_filters import rest_framework as filters
from datetime import datetime, timedelta
from django.db.models import F
from django.core.mail import send_mail



# HTTP Error 400
def bad_request(request,exception):
	response = render_to_response('polls/erros/400.html',context_instance=RequestContext(request))
	response.status_code = 400
	return response

def permission_denied(request,exception):
	response = render_to_response('polls/erros/403.html',context_instance=RequestContext(request))
	response.status_code = 403
	return response

def page_not_found(request,exception):
	response = render_to_response('polls/erros/400.html',context_instance=RequestContext(request))
	response.status_code = 404
	return response

def server_error(request):
	response = render_to_response('polls/erros/500.html',context_instance=RequestContext(request))
	response.status_code = 500
	return response


def pesquisa(request):
	template_name = 'polls/pesquisa.html'
	query = request.GET.get('q', '')
	prova = request.GET.get('prova', '')
	questao = request.GET.get('questao', '')
	categoria = request.GET.get('categoria', '')
	form = QuestaoProvaForm(prova, questao)
	# Filtro
	if categoria:
		categorias = Questao.objects.filter(idCategoria=categoria)
	respostas = Resposta.objects.filter(usuario=request.user)
	if request.method == 'POST':
		respostaform = RespostaForm(request.POST or None)
		if respostaform.is_valid():
			resp = respostaform.save(commit=False)
			resp.resposta = respostaform.cleaned_data['resposta']
			resp.usuario = request.user
			resp.idQuestao = request.POST.get('idQuestao')
			if resp.resposta == request.POST.get('idQuestao.respostaQuestao'):
				resp.certaresposta = 1
			else:
				resp.certaresposta = 0
			resp.save()
		return HttpResponseRedirect(request.path_info)
	else:
		respostaform = RespostaForm()
	try:
		if categoria == ('') and prova == ('') and questao == (''):
			results = Questao.objects.filter(Q(textoQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(cOpcao__icontains=query)| Q(dOpcao__icontains=query)| Q(eOpcao__icontains=query)).order_by('idProva')
		elif prova == ('') and prova == ('') and categoria != (''):
			results = Questao.objects.filter(Q(textoQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(cOpcao__icontains=query)| Q(dOpcao__icontains=query)| Q(eOpcao__icontains=query),idCategoria=categoria).order_by('idProva')
		elif questao == ('') and prova != ('') and categoria != (''):
			results = Questao.objects.filter(Q(textoQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(cOpcao__icontains=query)| Q(dOpcao__icontains=query)| Q(eOpcao__icontains=query), idProva=prova,idCategoria=categoria).order_by('idProva')
		elif questao == ('') and prova != ('') and categoria == (''):
			results = Questao.objects.filter(Q(textoQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(cOpcao__icontains=query)| Q(dOpcao__icontains=query)| Q(eOpcao__icontains=query), idProva=prova).order_by('idProva')
		elif questao != ('') and prova != ('') and categoria != (''):
			results = Questao.objects.filter(Q(textoQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(cOpcao__icontains=query)| Q(dOpcao__icontains=query)| Q(eOpcao__icontains=query), idQuestao=Questao).order_by('idProva')
		elif questao != ('') and prova != ('') and categoria == (''):
			results = Questao.objects.filter(Q(textoQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(cOpcao__icontains=query)| Q(dOpcao__icontains=query)| Q(eOpcao__icontains=query), idQuestao=questao,idProva=prova).order_by('idProva')
		else:
			results = Questao.objects.get(Q(textoQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(perguntaQuestao__icontains=query)| Q(cOpcao__icontains=query)| Q(dOpcao__icontains=query)| Q(eOpcao__icontains=query), idProva=prova,idQuestao=questao,idCategoria=categoria).order_by('idProva')
	except Questao.DoesNotExist:
		results = Questao.objects.all() 
	return render(request, template_name, {'form':form,'respostas':respostas,'respostaform':respostaform,'results': results,'prova':prova,'questao':questao,'questoes':questoes})
	#Q(idProva=prova)| Q(idQuestao=questao)| Q(idCategoria=categoria)

def index(request):
	provas = Prova.objects.all().order_by('idProva')
	questoes = Questao.objects.filter().order_by('idProva')
	categorias = Categoria.objects.all().order_by('nomeCategoria')
	return render(request, 'polls/index.html',{'categorias':categorias,'questoes':questoes,'provas':provas})

def desempenho(request):
	pontos = int(request.user.usuario.pontos)
	questoes = int(Questao.objects.filter(tipoQuestao=1).count())
	pq = pontos/questoes
	respostas = Resposta.objects.filter(usuario=request.user)
	respostascertas = Resposta.objects.filter(usuario=request.user,certaresposta=True).count()
	respostasME = Resposta.objects.filter(Q(resposta="A") | Q(resposta="B")| Q(resposta="C")| Q(resposta="D")| Q(resposta="E"),usuario=request.user).count() - respostascertas
	return render(request, 'polls/desempenho.html',{'respostas':respostas,'pq':pq,'questoes':questoes,'pontos':pontos,'respostascertas':respostascertas,'respostasME':respostasME})

def get_data(request):
	provas = Prova.objects.all()
	prova = request.POST.get("prova")
	categoria = request.POST.get("categoria")
	questoes = Questao.objects
	return render(request,"polls/exam.html",{'provas':provas})


@login_required()
def seletor_quiz(request):
	provas = Prova.objects.all().order_by('idProva')
	categorias = Categoria.objects.all().order_by('nomeCategoria')
	num_questoes = Questao.objects.filter(tipoQuestao=1).count()+1
	lista_questoes = []
	for i in range(1,num_questoes):
		lista_questoes.append(i)
	return render(request, 'polls/seletor_quiz.html', {'lista_questoes':lista_questoes,'provas':provas,'categorias':categorias,'num_questoes':num_questoes})


def desempenho_disciplinas(request):
	usuario = Usuario.objects.get(user=request.user)
	questoes = Questao.objects.filter(statusQuestao=1,idCategoria__in=[idCategoria for idCategoria in usuario.idCategoria.all()]).count()
	categoria = Categoria.objects.filter(usuario__user=request.user)
	respostas = Resposta.objects.filter(idQuestao__idCategoria__in=categoria)
	respostascertas = Resposta.objects.filter(idQuestao__idCategoria__in=categoria,certaresposta=True).count()
	respostasME = respostas.count() - respostascertas
	return render(request, 'polls/desempenho_disciplinas.html',{'respostas':respostas,'questoes':questoes,'respostascertas':respostascertas,'respostasME':respostasME})


def lista_aprovacao(request):
	usuario = Usuario.objects.get(user=request.user)
	questoes = Questao.objects.filter(statusQuestao=2,idCategoria__in=[idCategoria for idCategoria in usuario.idCategoria.all()])
	return render(request, 'polls/lista_aprovacao.html', {'questoes':questoes})

def detalhes(request, idProva):
	prova = get_object_or_404(Prova,pk=idProva)
	model = Prova
	context_object_name = 'prova'
	queryset = Prova.objects.all()
	questoes = Questao.objects.filter()
	return render(request, 'polls/detalhes.html', {'questoes':questoes,'prova': prova})


def lista_categorias(request):
	categorias = Categoria.objects.all().order_by('nomeCategoria')
	context = {'categorias': categorias}
	return render(request, 'polls/lista_categorias.html', context=context)

def questoes_ajax(request):
	prova = request.GET.get('prova',None)
	if prova:
		questoes = Questao.objects.filter(idProva=prova)
	else:
		questoes = Questao.objects.all()
	context = {'questoes': questoes}
	return render(request, 'polls/includes/_questoes.html', context)

def questoes_choices_ajax(request):
	prova = request.GET.get('prova',None)
	if prova:
		questoes = Questao.objects.filter(idProva=prova)
	else:
		questoes = Questao.objects.all()
	context = {'questoes': questoes}
	return render(request, 'polls/includes/_questoes_choices.html', context)

def filter_dropdown2(request):
	context = {}
	prova = request.GET.get('prova')
	questao = request.GET.get('questao')
	context['form'] = QuestaoProvaForm(prova, questao)
	# Filtro
	categoria = request.GET.get('categoria')
	if categoria:
		categorias = Questao.objects.filter(idCategoria=categoria)
		context['categorias'] = categorias
	return render(request, 'polls/filter_dropdown2.html', context)


def categorias_ajax(request):
	questao = request.GET.get('questao')
	categorias = Categoria.objects.filter(questao=questao)
	context = {'categorias': categorias}
	return render(request, 'polls/includes/_categorias.html', context)


def categorias_choices_ajax(request):
	questao = request.GET.get('questao')
	categorias = categoria.objects.filter(questao=questao)
	context = {'categorias': categorias}
	return render(request, 'polls/includes/_categorias_choices.html', context)

def resultado(request, idProva, idQuestao):
	questao = get_object_or_404(Questao, pk=idQuestao)
	prova = get_object_or_404(Prova, pk=idProva)
	return render(request, 'polls/resultado.html', {'questao': questao,'prova':prova})

def categoria(request,idCategoria):
	categorias = Categoria.objects.all()
	questao = Questao.objects.filter(statusQuestao='1')
	if idCategoria:
		categoria = get_object_or_404(Categoria,pk=idCategoria)
		questao = questao.filter(idCategoria=categoria)
	template = 'polls/categorias.html'
	context = {'categorias':categorias,'questao':questao,'categoria':categoria}
	return render(request,template, context)


def json_provaple(request):
	return render(request, 'json_provaple.html')

def chart_data(request):
	dataset = Passenger.objects \
		.values('embarked') \
		.filter(embarked='') \
		.annotate(total=Count('embarked')) \
		.order_by('embarked')

	port_display_name = dict()
	for port_tuple in Passenger.PORT_CHOICES:
		port_display_name[port_tuple[0]] = port_tuple[1]

	chart = {
		'chart': {'type': 'pie'},
		'title': {'text': 'Titanic Survivors by Ticket Class'},
		'series': [{
			'name': 'Embarkation Port',
			'data': list(map(lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']}, dataset))
		}]
	}

	return JsonResponse(chart)

def quiz(request):
	prova = request.GET.get("prova",'')
	qtd = request.GET.get('qtd',None)
	categoria = request.GET.get("categoria",'')
	if categoria != ('') and prova != (''):
		questao = Questao.objects.annotate(resp_count=models.Count(models.Case(models.When(resposta__usuario=request.user, then=1),output_field=models.IntegerField()))).filter(resp_count=0,tipoQuestao=1,statusQuestao=1,idProva=prova,idCategoria=categoria).order_by("?").first()
	elif categoria == ('') and prova != (''):
		questao = Questao.objects.annotate(resp_count=models.Count(models.Case(models.When(resposta__usuario=request.user, then=1),output_field=models.IntegerField()))).filter(resp_count=0,tipoQuestao=1,statusQuestao=1,idProva=prova).order_by("?").first()
	elif categoria != ('') and prova == (''):
		questao = Questao.objects.annotate(resp_count=models.Count(models.Case(models.When(resposta__usuario=request.user, then=1),output_field=models.IntegerField()))).filter(resp_count=0,tipoQuestao=1,statusQuestao=1,idCategoria=categoria).order_by("?").first()
	else:
		questao = Questao.objects.annotate(resp_count=models.Count(models.Case(models.When(resposta__usuario=request.user, then=1),output_field=models.IntegerField()))).filter(resp_count=0,tipoQuestao=1,statusQuestao=1).order_by("?").first()
	q = request.POST.get('idQuestao',None)
	respostas = Resposta.objects.filter(usuario=request.user,idQuestao=questao)
	respostaform = RespostaForm(request.GET,request.POST or None)
	qtdrespostas = Resposta.objects.filter(idQuestao=q).count()
	qtdrespostascertas = Resposta.objects.filter(idQuestao=q,certaresposta=True).count()
	if qtdrespostas:
		pq = qtdrespostascertas/qtdrespostas
	else:
		pq = 1
	data = datetime.now() + timedelta(minutes=2)
	if request.method == 'POST':
		if respostaform.is_valid():
			resp = respostaform.save(commit=False)
			resp.resposta = request.POST.get('resposta','')
			resp.usuario = request.user
			resp.idQuestao_id = q
			if resp.resposta == questao.respostaQuestao:
				resp.certaresposta = True
				Usuario.objects.filter(user=request.user).update(pontos=F("pontos") + 1)
			else:
				resp.certaresposta = False
			resp.save()
		return redirect('/quiz/?prova=%s&categoria=%s' % (prova,categoria) )
	else:
		respostaform = RespostaForm()
	return render(request, 'polls/quiz.html', {'qtdrespostas':qtdrespostas,'qtdrespostascertas':qtdrespostascertas,'pq':pq,'q':q,'respostaform': respostaform,'questao':questao,'respostas': respostas})


def add_questoes(request):
	if request.method == 'POST': # If the form has been submitted...
		form = QuestaoForm(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			form.save()
			subject = 'Questão adicionada'
			message = 'Há uma nova questão adicionada'
			recepient = str(sub['Email'].value())
			send_mail(subject, 
				message, EMAIL_HOST_USER, [recepient], fail_silently = False)
		return redirect('/') # Redirect after POST
	else:
		form = QuestaoForm() # An unbound form
	return render(request, 'polls/add_questoes.html', {'form': form})

def add_provas(request):
	if request.method == 'POST':
		form = ProvaForm(request.POST or None)
		if form.is_valid():
			prova = form.save(commit=False)
			prova.idProva = form.cleaned_data.get('idQuestao')
			prova.tipoProva = form.cleaned_data.get('tipoProva')
			prova.anoProva = form.cleaned_data.get('anoProva')
			prova.save()
		return redirect('/')
	else:
		form = ProvaForm()
	return render(request,'polls/add_provas.html',{'form':form})



def get_showrooms(request, **kwargs):
	brand = Brands.objects.get(id=kwargs['brand_id'])
	showroom_list = list(brand.showrooms.values('id', 'name'))

	return HttpResponse(simplejson.dumps(showroom_list), content_type="application/json")

def add_categorias(request):
	if request.method == 'POST':
		form = CategoriaForm(request.POST or None)
		if form.is_valid():
			cat = form.save(commit=False)
			cat.idCategoria = form.cleaned_data.get('idCategoria')
			cat.nomeCategoria = form.cleaned_data.get('nomeCategoria')
			cat.parent = form.cleaned_data.get('parent')
			cat.save()
		return redirect('/')
	else:
		form = CategoriaForm()
	return render(request,'polls/add_categorias.html',{'form':form})

def questoes(request, idQuestao,idProva):
	totalRespostas = Resposta.objects.filter(idQuestao=idQuestao)
	A = Resposta.objects.filter(idQuestao=idQuestao,resposta='A')
	B = Resposta.objects.filter(idQuestao=idQuestao,resposta='B')
	C = Resposta.objects.filter(idQuestao=idQuestao,resposta='C')
	D = Resposta.objects.filter(idQuestao=idQuestao,resposta='D')
	E = Resposta.objects.filter(idQuestao=idQuestao,resposta='E')
	Aresposta = Resposta.objects.filter(idQuestao=idQuestao,usuario=request.user,resposta='1')
	Bresposta = Resposta.objects.filter(idQuestao=idQuestao,usuario=request.user,resposta='2')
	Cresposta = Resposta.objects.filter(idQuestao=idQuestao,usuario=request.user,resposta='3')
	Dresposta = Resposta.objects.filter(idQuestao=idQuestao,usuario=request.user,resposta='4')
	Eresposta = Resposta.objects.filter(idQuestao=idQuestao,usuario=request.user,resposta='5')
	prova = get_object_or_404(Prova,pk=idProva)
	questao = get_object_or_404(Questao,pk=idQuestao)
	lista_de_questoes = Questao.objects.filter()
	respostas = Resposta.objects.filter(idQuestao=idQuestao,usuario=request.user)
	qtdrespostas = Resposta.objects.filter(idQuestao=idQuestao).count()
	qtdrespostascertas = Resposta.objects.filter(idQuestao=idQuestao,certaresposta=True).count()
	if qtdrespostas:
		pq = qtdrespostascertas/qtdrespostas
	else:
		pq = 1
	if request.user.usuario.tipoUsuario == 2:
		form = AprovaForm(request.POST,request.GET,instance=questao)
		if request.method == 'POST':
			print (form.instance)
			if form.is_valid():
				model_instance = form.save(commit=False)
				model_instance.statusQuestao = form.cleaned_data.get('statusQuestao')
				model_instance.save()
			else:
				form = AprovaForm()
	else:
		form = RespostaForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				resp = respostaform.save(commit=False)
				if questao.tipoQuestao == 2:
					resp.respostaA = form.cleaned_data['respostaA']
					resp.respostaB = form.cleaned_data['respostaB']
					resp.respostaC = form.cleaned_data['respostaC']
					resp.respostaD = form.cleaned_data['respostaD']
					resp.respostaE = form.cleaned_data['respostaE']
					if resp.respostaA != (''):
						resp.resposta = ''
					elif resp.respostaB != (''):
						resp.resposta = '2'
					elif resp.respostaC != (''):
						resp.resposta = '3'
					elif resp.respostaD != (''):
						resp.resposta = '4'
					elif resp.respostaE != (''):
						resp.resposta = '5'
				else:
					resp.resposta = form.cleaned_data['resposta']
					if resp.resposta == questao.respostaQuestao:
						resp.certaresposta = True
						Usuario.objects.filter(user=request.user).update(pontos=F("pontos") + 1)
					else:
						resp.certaresposta = False
				resp.usuario = request.user
				resp.idQuestao = questao
				resp.save()
			return HttpResponseRedirect(request.path_info)
		else:
			form = RespostaForm()
	return render(request, 'polls/questoes.html', {'pq':pq,'qtdrespostascertas':qtdrespostascertas,'qtdrespostas':qtdrespostas,'Eresposta':Eresposta,'Dresposta':Dresposta,'Cresposta':Cresposta,'Bresposta':Bresposta,'Aresposta':Aresposta,'A':A,'B':B,'C':C,'D':D,'E':E,'totalRespostas':totalRespostas,'questao':questao,'prova': prova,'respostas': respostas,'form':form})
	
def user_login(request):
	usuario = Usuario.objects.create(user=request.user)
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'],
					password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponse('Autenticado','com sucesso')
				else:
					return HttpResponse('Conta desabilitada')
			else:
				return HttpResponse('Login inválido')
	else:
		form = LoginForm()
	return render(request, 'polls/login.html', {'form': form})

def logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('/'))

def alterarsenha(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)	# Important!
			messages.success(request, 'Sua senha foi alterada com sucesso!')
			return redirect('/')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'polls/alterarsenha.html', {'form': form})

def thanks(request):
	return render(request,'polls/thanks.html')


def registrar(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST,request.FILES)
		if form.is_valid():
			user = form.save(commit=False)
			user.usuario.avatar = form.cleaned_data.get('avatar')
			user.refresh_from_db()
			user.first_name = form.cleaned_data.get('first_name')
			user.last_name = form.cleaned_data.get('last_name')
			user.usuario.matricula = form.cleaned_data.get('matricula')
			user.usuario.tipoUsuario = form.cleaned_data.get('tipoUsuario')
			if user.usuario.tipoUsuario == 1:
				user.save()
			else:
				user.usuario.idCategoria.set(form.cleaned_data.get("idCategoria"))
				user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('/')
		else:
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'polls/registrar.html', {'form': form})

def profile_view(request):
	user = request.user
	form = EditProfileForm(initial={'first_name':user.first_name, 'last_name':user.last_name})
	context = {"form": form}
	return render(request, 'polls/profile.html', context)

@login_required
def edit_profile(request):
	if request.method == 'POST':
		form = UserForm(request.POST,request.FILES,instance=request.user)
		profile_form = UsuarioForm(request.POST, request.FILES, instance=request.user.usuario)
		if form.is_valid() and profile_form.is_valid():
			form = form.save()
			custom_form = profile_form.save(False)
			custom_form.user = form
			custom_form.save()
			if custom_form.user.usuario.tipoUsuario == 2:
				custom_form.idCategoria.set(profile_form.cleaned_data['idCategoria'])
				custom_form.save()
			return redirect('/perfil')
	else:
		form = UserForm(instance=request.user)
		profile_form = UsuarioForm(instance=request.user.usuario)
	context = {'form': form,'profile_form':profile_form}
	return render(request, 'polls/edit_profile.html', context)

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_list = 'lista_de_provas'

	def get_queryset(self):
		return Prova.objects.order_by('anoProva')[:5]

class QuestaoViewset(viewsets.ModelViewSet):
	queryset = Questao.objects.all()
	serializer_class = QuestaoSerialzer


class ProvaViewset(viewsets.ModelViewSet):
	queryset = Prova.objects.all()
	serializer_class = ProvaSerializer

class ProvaQuestaoViewset(viewsets.ModelViewSet):
	serializer_class = QuestaoSerialzer
	queryset = Questao.objects.filter(tipoQuestao=1)
	def get_queryset(self):
		return Questao.objects.filter(idProva=self.kwargs.get('idQuestao'))

class QuizView(generic.DetailView):
	model = Questao
	context_object_name = 'questao'