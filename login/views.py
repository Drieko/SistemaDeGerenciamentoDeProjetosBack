# login/views.py
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializer import UserSerializer
from .models import User


class UserCreateView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['nome', 'email', 'senha'],
        properties={
                'nome': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do usuário'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail do usuário'),
                'senha': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário')
            }
        ),
        responses={201: 'Usuário criado com sucesso'}
    )
    
    def post(self, request, *args, **kwargs):        
        nome = request.data.get('nome')
        email = request.data.get('email')
        senha = request.data.get('senha')
        
        if User.objects.filter(email=email).exists():
            return HttpResponse('E-mail ja está sendo usado.')
        # Criando o usuário com o método personalizado
        user = User.objects.create(nome=nome, email=email, senha=make_password(senha))
        user.save()
        
        return Response({"message": "Usuário criado com sucesso!"}, status=status.HTTP_201_CREATED)
    
    class LoginView(APIView):
        @swagger_auto_schema(
                request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, 
            required=['email','senha'],
             properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='E-mail do usuário'),
                'senha': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário')
            }
        ),
        responses={200: 'Token de autenticação'}
    )
                
        
        def post(self, request, *args, **kwargs):
            email = request.data.get('email')
            senha = request.data.get('senha')

            # Encontrar o usuário 
            user = User.objects.filter(email=email).first()

            if user and user.check_password(senha):  # Verificando se a senha é válida
                refresh = RefreshToken.for_user(user)  # Gerando o token
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })

            return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_400_BAD_REQUEST)
