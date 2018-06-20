# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Prova, Questao, Opcao, Resposta, Usuario
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .forms import UsuarioForm, LoginForm, ProvaForm, AlterarSenhaForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login, logout, authenticate
from django.utils.translation import ugettext as _




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

	model = Prova
	template_name = 'polls/detalhes.html'  # Default: <app_label>/<model_name>_list.html
	context_object_name = 'prova'  # Default: object_list
	paginate_by = 10
	queryset = Prova.objects.all()

	try:
		questao_selec = prova.questao_set.get(pk=request.POST['questao'])
		pagina = paginator.page(page)
	except (KeyError,Questao.DoesNotExist):
		return render (request,'polls/detalhes.html',{
			'prova': prova,
		})
	except PageNotAnInteger:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	else:
		#questao_selec.votes += 1
		questao_selec = Questao(textoQuestao=request.POST.get('textoQuestao'),imagemQuestao=request.FILES('imagemQuestao'),imagem2Questao=request.FILES('imagem2Questao'),perguntaQuestao=request.POST.get('perguntaQuestao'))
		questao_selec.save()
		return HttpResponseRedirect(reverse('polls:resultados',args=(prova.idProva,)))
	
def questoes(request, idQuestao,idProva):
	prova = get_object_or_404(Prova,pk=idProva)
	questao = get_object_or_404(Questao,pk=idQuestao)
	lista_de_questoes = Questao.objects.filter()
	try:
		questao_selec = prova.questao_set.get(pk=request.POST['questao'])
		opcao_selec = questao.opcao_set.get(pk=request.POST['opcao'])
	except (KeyError,Questao.DoesNotExist):
		return render (request,'polls/questoes.html',{
			'prova': prova,
			'questao': questao,
		})
	else:
		#questao_selec.votes += 1
		questao_selec = Questao(textoQuestao=request.POST.get('textoQuestao'),imagemQuestao=request.FILES('imagemQuestao'),imagem2Questao=request.FILES('imagem2Questao'),perguntaQuestao=request.POST.get('perguntaQuestao'))
		questao_selec.save()
		return HttpResponseRedirect(reverse('polls:resultados',args=(questao.idQuestao)))


def resposta(request,idQuestao):
	questao = get_object_or_404(Questao,pk=idQuestao)
	opcao = get_object_or_404(Opcao,pk=idOpcao)
	try:
		resposta_selec = opcao.resposta_set.get(pk=request.POST['gabarito'])
	except (KeyError,Gabarito.DoesNotExist):
		return render (request,'polls/resposta.html',{
			'opcao': opcao,
		})
	else:
		resposta_selec.save()
		return HttpResponseRedirect(reverse('polls:resposta',args=(opcao.idOpcao,)))
	#return render(request,'polls/resposta.html')	
	






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
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('polls/alterarsenha')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'polls/alterarsenha.html', {
		'form': form
	})


def thanks(request):
	return render(request,'polls/thanks.html')


def registrar(request):
	if request.method == 'POST':
		form = UsuarioForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = UsuarioForm()
	return render(request, 'polls/registrar.html', {'form': form})



class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_list = 'lista_de_provas'

	def get_queryset(self):
		return Prova.objects.order_by('anoProva')[:5]

class DetailView(generic.DetailView):
	model = Prova
	template_name = 'polls/detalhes.html'