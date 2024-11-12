from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nome', 'email', 'senha']
        extra_kwargs = {
            'senha': {'write_only': True},  # A senha não será retornada nos resultados
        }