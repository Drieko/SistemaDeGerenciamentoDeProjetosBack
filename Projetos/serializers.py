from rest_framework import serializers
from .models import Projetos
from .models import Tarefas

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projetos
        fields = ['id', 'titulo', 'description', 'prazo', 'created', 'status']


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = ['id', 'titulo', 'description', 'prazo', 'created', 'prioridade', 'projeto']
