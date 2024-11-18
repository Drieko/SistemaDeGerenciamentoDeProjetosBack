from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Projetos, Tarefas
from .serializers import ProjetoSerializer, TarefaSerializer
from drf_yasg.utils import swagger_auto_schema


class ProjetoView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Garante que o usuário está autenticado

    @swagger_auto_schema(responses={200: 'Lista de projetos'})
    def get(self, request):
        """
        Listar projetos do usuário autenticado com filtro por status.
        """
        status_filter = request.query_params.get('status', None)
        projetos = Projetos.objects.filter(usuarios=request.user)  # Filtra projetos associados ao usuário

        if status_filter:
            projetos = projetos.filter(status=status_filter)

        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProjetoSerializer, responses={201: 'Projeto criado'})
    def post(self, request):
        """
        Criar um novo projeto e associar ao usuário autenticado.
        """
        # Associar automaticamente o usuário autenticado ao projeto
        serializer = ProjetoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(usuarios=[request.user])  # Adiciona o usuário autenticado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProjetoIdView(APIView):
    @swagger_auto_schema(responses={200: ProjetoSerializer})
    def get(self, request, pk=None):
        try:
            projeto = Projetos.objects.get(pk=pk, usuarios=request.user)  # Filtra pelo usuário autenticado
        except Projetos.DoesNotExist:
            return Response({"detail": "Projeto não encontrado ou você não tem permissão para visualizá-lo."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ProjetoSerializer(projeto)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ProjetoSerializer, responses={200: ProjetoSerializer})
    def put(self, request, pk=None):
        """
        Atualiza um projeto existente.
        """
        try:
            projeto = Projetos.objects.get(pk=pk, usuarios=request.user)  # Filtra pelo usuário autenticado
        except Projetos.DoesNotExist:
            return Response({"detail": "Projeto não encontrado ou você não tem permissão para editá-lo."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = ProjetoSerializer(projeto, data=request.data, partial=False)  # False se for obrigatório atualizar todos os campos
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(responses={204: 'Projeto excluído'})
    def delete(self, request, pk=None):
        try:
            projeto = Projetos.objects.get(pk=pk, usuarios=request.user)  # Filtra pelo usuário autenticado
        except Projetos.DoesNotExist:
            return Response({"detail": "Projeto não encontrado ou você não tem permissão para excluí-lo."},
                            status=status.HTTP_404_NOT_FOUND)
        projeto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#tarefas 
class TarefaView(APIView):
    @swagger_auto_schema(responses={200: 'Lista de tarefas'})
    def get(self, request):
        tarefas = Tarefas.objects.all()
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TarefaSerializer, responses={201: 'Tarefa criada'})
    def post(self, request):
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
