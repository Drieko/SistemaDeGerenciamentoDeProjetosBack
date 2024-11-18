from rest_framework import serializers
from .models import Projetos
from .models import Tarefas
from django.contrib.auth.models import User

class ProjetoSerializer(serializers.ModelSerializer):
    usuarios = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = Projetos
        fields = '__all__'


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'
