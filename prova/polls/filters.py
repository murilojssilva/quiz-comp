from .models import Questao
import django_filters
from rest_framework.filters import OrderingFilter


class FiltroQuestoes(django_filters.FilterSet):
	class Meta:
		model = Questao
		fields = ['textoQuestao','perguntaQuestao','aOpcao','bOpcao','cOpcao','dOpcao','eOpcao','idProva','idQuestao','idCategoria']