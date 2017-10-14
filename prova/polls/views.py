# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Prova, Questao, Opcao, Resposta, Usuario
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UsuarioForm, LoginForm, ProvaForm, AlterarSenhaForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, logout, authenticate



def index(request):
	lista_de_provas = Prova.objects.filter()
	cprova = request.POST.get('idProva')
	if request.method == 'POST':
		sprova = Prova.objects.get(cprova = cprova)
		sprova.select()
		return redirect('polls/detalhes.html')
	else:
		form = ProvaForm()
	return render(request, 'polls/index.html',{'form':form,'lista_de_provas': lista_de_provas})

	
def detalhes(request, idProva):
	prova = get_object_or_404(Prova,pk=idProva)
	try:
		questao_selec = prova.questao_set.get(pk=request.POST['questao'])
	except (KeyError,Questao.DoesNotExist):
		return render (request,'polls/detalhes.html',{
			'prova': prova,
		})
	else:
		#questao_selec.votes += 1
		questao_selec = Questao(textoQuestao=request.POST.get('textoQuestao'),imagemQuestao=request.FILES('imagemQuestao'),imagem2Questao=request.FILES('imagem2Questao'),perguntaQuestao=request.POST.get('perguntaQuestao'))
		questao_selec.save()
		return HttpResponseRedirect(reverse('polls:resultados',args=(prova.idProva,)))
	
	questao = get_object_or_404(Questao,pk=idQuestao)
	try:
		opcao_selec = questao.opcao_set.get(pk=request.POST['opcao'])
	except (KeyError,Opcao.DoesNotExist):
		return render (request,'polls/detalhes.html',{
			'questao': questao,
		})
	else:
		#opcao_selec.votes += 1

		opcao_selec.save()
		return HttpResponseRedirect(reverse('polls:resultados',args=(questao.idQuestao,)))




def user_login(request):
	if request.method == 'POST':
		logar = LoginForm(data=request.POST)
		if logar.is_valid():
			login(request, logar.get_user())
			return HttpResponseRedirect("/")
		else:
			return render(request, 'polls/thanks.html', {"logar": logar})
	return render(request, 'polls/login.html', {"logar": LoginForm()})


def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			matriculaUsuario = form.cleaned_data.get("matriculaUsuario")
			senhaUsuario = form.cleaned_data.get("senhaUsuario")
			user = authenticate(matriculaUsuario=matriculaUsuario,senhaUsuario=senhaUsuario)
			if user is not None:
				if user.is_active:
					login(request, user)
					return render(request, 'polls/thanks.html')
				else:
					return render(request, 'polls/login.html', {"form": form})
			else:
				return render(request, 'polls/registrar.html', {"form": form})
	else:
		form = LoginForm()
	return render(request, 'polls/login.html', {'form': form})



def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('/'))



def alterarsenha(request):
	if request.method == 'POST':
		form = AlterarSenhaForm(request.usuario, request.POST)
		if form.is_valid():
			usuario = form.save()
			update_session_auth_hash(request, usuario)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('alterarsenha')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = AlterarSenhaForm(request.usuario)
	return render(request, 'polls/alterarsenha.html', {
		'form': form
    })


def thanks(request):
	return render(request,'polls/thanks.html')



def resposta(request):
	opcao = get_object_or_404(Opcao,pk=idOpcao)
	try:
		resposta_selec = opcao.gabarito_set.get(pk=request.POST['gabarito'])
	except (KeyError,Gabarito.DoesNotExist):
		return render (request,'polls/resposta.html',{
			'opcao': opcao,
		})
	else:
		resposta_selec.save()
		return HttpResponseRedirect(reverse('polls:resposta',args=(opcao.idOpcao,)))
	#return render(request,'polls/resposta.html')



def registrar(request):
	if request.method == 'POST':
		registro =UsuarioForm(request.POST)
		if registro.is_valid():
			registro.save()
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/registrar/')
	else:
		registro = UsuarioForm()
		return render(request, 'polls/registrar.html',{'registro':registro})



class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_list = 'lista_de_provas'

	def get_queryset(self):
		return Prova.objects.order_by('anoProva')[:5]

class DetailView(generic.DetailView):
	model = Prova
	template_name = 'polls/detalhes.html'