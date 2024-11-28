from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ComentarioProjeto, ComentarioTarefa, Projetos, Tarefas, Convites

class ComentarioProjetoSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)  # Exibe o nome do autor
    data_criacao = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # Formata a data

    class Meta:
        model = ComentarioProjeto
        fields = '__all__'

    def create(self, validated_data):
        # Preenche automaticamente o campo 'autor' com o usuário autenticado
        validated_data['autor'] = self.context['request'].user
        return super().create(validated_data)

class ComentarioTarefaSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)  # Exibe o nome do autor
    data_criacao = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # Formata a data

    class Meta:
        model = ComentarioTarefa
        fields = '__all__'

    def create(self, validated_data):
        # Preenche automaticamente o campo 'autor' com o usuário autenticado
        validated_data['autor'] = self.context['request'].user
        return super().create(validated_data)
    
class ProjetoSerializer(serializers.ModelSerializer):
    usuarios = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model = Projetos
        fields = '__all__'


class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefas
        fields = '__all__'
        

class ConviteSerializer(serializers.ModelSerializer):
    # Definindo os campos do modelo que queremos exibir no Swagger.
    enviado_por = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recebido_por = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    projeto = serializers.PrimaryKeyRelatedField(queryset=Projetos.objects.all())
    status = serializers.CharField(default='pendente')
    data_envio = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)

    class Meta:
        model = Convites
        fields = ['id', 'enviado_por', 'recebido_por', 'projeto', 'status', 'data_envio']