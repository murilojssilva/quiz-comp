from rest_framework import serializers

from polls.models import Prova, Questao


class ProvaSerializer(serializers.ModelSerializer):
	class Meta:
		model = Prova
		fields = ['idProva','tipoProva','anoProva']

class QuestaoSerialzer(serializers.ModelSerializer):
	class Meta:
		model = Questao
		fields = ['imagemQuestao','imagemQuestao2','textoQuestao','perguntaQuestao','respostaQuestao','idQuestao','aOpcao','bOpcao','cOpcao','dOpcao','eOpcao','idProva']