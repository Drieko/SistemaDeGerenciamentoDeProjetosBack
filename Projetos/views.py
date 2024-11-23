from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Projetos, Tarefas, Comentario
from .serializers import ProjetoSerializer, TarefaSerializer, ComentarioSerializer
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
            serializer.save()  # Adiciona o usuário autenticado
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
    
class TarefaIdView(APIView):
    @swagger_auto_schema(responses={200: TarefaSerializer})
    def get(self, request, pk=None):
        try:
            tarefa = Tarefas.objects.get(id=pk,  projeto__usuarios=request.user)  # Filtra pelo usuário autenticado
        except Tarefas.DoesNotExist:
            return Response({"detail": "Projeto não encontrado ou você não tem permissão para visualizá-lo."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TarefaSerializer, responses={200: TarefaSerializer})
    def put(self, request, pk=None):
        """
        Atualiza um Tarefa existente.
        """
        try:
            tarefa = Tarefas.objects.get(id=pk, projeto__usuarios=request.user)  # Filtra pelo usuário autenticado
        except Tarefas.DoesNotExist:
            return Response({"detail": "tarefa não encontrado ou você não tem permissão para editá-lo."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = TarefaSerializer(tarefa, data=request.data, partial=False)  # False se for obrigatório atualizar todos os campos
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(responses={204: 'tarefa excluído'})
    def delete(self, request, pk=None):
        try:
            tarefa = Tarefas.objects.get(id=pk, projeto__usuarios=request.user)  # Filtra pelo usuário autenticado
        except Tarefas.DoesNotExist:
            return Response({"detail": "tarefa não encontrado ou você não tem permissão para excluí-lo."},
                            status=status.HTTP_404_NOT_FOUND)
        tarefa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ComentarioView(APIView):
    class Meta:
        extra_kwargs = {'tarefa': {'required': False}, 'projeto': {'required': False}}
    @swagger_auto_schema(
        operation_summary='Retorna os comentários de uma tarefa ou projeto.',
        responses={
            200: ComentarioSerializer(many=True),
            400: 'Tipo inválido, use "tarefa" ou "projeto".',
            404: 'Tarefa ou projeto não encontrado.'
        }
    )
    def get(self, request, pk=None, tipo='tarefa'):
        if tipo == 'tarefa':
            try:
                tarefa = Tarefas.objects.get(pk=pk)
                comentarios = Comentario.objects.filter(tarefa=tarefa)
            except Tarefas.DoesNotExist:
                return Response({"detail": "Tarefa não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        elif tipo == 'projeto':
            try:
                projeto = Projetos.objects.get(pk=pk)
                comentarios = Comentario.objects.filter(projeto=projeto)
            except Projetos.DoesNotExist:
                return Response({"detail": "Projeto não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Tipo inválido, use 'tarefa' ou 'projeto'."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ComentarioSerializer(comentarios, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Cria um novo comentário.',
        request_body=ComentarioSerializer,
        responses={
            201: ComentarioSerializer,
            400: 'Dados inválidos.',
            404: 'Tarefa ou projeto não encontrado.'
        }
    )
    def post(self, request, pk=None, tipo='tarefa'):
        if tipo == 'tarefa':
            try:
                tarefa = Tarefas.objects.get(pk=pk)
            except Tarefas.DoesNotExist:
                return Response({"detail": "Tarefa não encontrada"}, status=status.HTTP_404_NOT_FOUND)
        elif tipo == 'projeto':
            try:
                projeto = Projetos.objects.get(pk=pk)
            except Projetos.DoesNotExist:
                return Response({"detail": "Projeto não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Tipo inválido, use 'tarefa' ou 'projeto'."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tarefa=tarefa) if tipo == 'tarefa' else serializer.save(projeto=projeto)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComentarioIdView(APIView):
    def delete(self, request, pk=None):
        """
        Exclui um comentário específico.
        """
        try:
            comentario = Comentario.objects.get(pk=pk, autor=request.user)
        except Comentario.DoesNotExist:
            return Response({"detail": "Comentário não encontrado ou você não tem permissão para excluí-lo."},
                            status=status.HTTP_404_NOT_FOUND)

        comentario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
