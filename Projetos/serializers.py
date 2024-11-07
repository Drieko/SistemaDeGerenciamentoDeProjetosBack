from rest_framework import serializers
from .models import Projetos

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projetos
        fields = ['id', 'titulo', 'description', 'prazo', 'created', 'status']