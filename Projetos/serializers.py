from rest_framework import serializers
from .models import Projetos
from .models import Tarefas
from django.contrib.auth.models import User
from .models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)  # Exibe o nome do autor
    data_criacao = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # Formata a data

    class Meta:
        model = Comentario
        fields = '__all__'

class ProjetoSerializer(serializers.ModelSerializer):
    usuarios = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = Projetos
        fields = '__all__'


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'
        extra_kwargs = {
            'tarefa': {'required': False, 'allow_null': True},
            'projeto': {'required': False, 'allow_null': True}
        }
