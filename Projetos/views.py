from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Projetos, Tarefas, ComentarioProjeto, ComentarioTarefa, Convites
from .serializers import ProjetoSerializer, TarefaSerializer, ComentarioProjetoSerializer, ComentarioTarefaSerializer, ConviteSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

class ProjetoStatusView(APIView):
    STATUS_CHOICES = [
    ('andamento', ('Em andamento')),
    ('cancelado', ('Cancelado')),
    ('concluido', ('Concluído')),
    ]

    @swagger_auto_schema(
    operation_summary='Retorna os projetos com base no status.',
    manual_parameters=[
        openapi.Parameter(
            name='status',
            in_=openapi.IN_QUERY,
            description='Status dos projetos.',
            type=openapi.TYPE_STRING,
            enum=[status[0] for status in STATUS_CHOICES]
        )
    ],
    responses={
        200: ProjetoSerializer(many=True),
        400: 'Status inválido.',
        404: 'Nenhum projeto encontrado com o status especificado.'
    })
    def get(self, request, pk=None):
        """
        Retorna os projetos com base no status.
        """
        status = request.query_params.get('status')

        if status:
            projetos = Projetos.objects.filter(status=status)
        else:
            projetos = Projetos.objects.all()

        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)
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

class ComentarioProjetoView(APIView):
    @swagger_auto_schema(
        operation_summary='Retorna os comentários de um projeto.',
        responses={
            200: ComentarioProjetoSerializer(many=True),
            400: 'Tipo inválido, use "projeto".',
            404: 'Projeto não encontrado.'
        }
    )
    def get(self, request, pk):
        """
        Retorna todos os comentários de um projeto específico.
        """
        try:
            projeto = Projetos.objects.get(id=pk)
            comentarios = ComentarioProjeto.objects.filter(projeto=projeto)
        except Projetos.DoesNotExist:
            return Response({"detail": "Projeto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ComentarioProjetoSerializer(comentarios, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Cria um novo comentário para um projeto.',
        request_body=ComentarioProjetoSerializer,
        responses={
            201: ComentarioProjetoSerializer,
            400: 'Dados inválidos.',
            404: 'Projeto não encontrado.'
        }
    )
    def post(self, request, pk=None):
        """
        Cria um novo comentário associado a um projeto específico.
            """
        try:
            projeto = Projetos.objects.get(id=request.data['projeto'])
            
        except Projetos.DoesNotExist:
            return Response({"detail": "Projeto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if not projeto:
            return Response({"detail": "Projeto não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Associando o projeto ao comentário
        # request.data['projeto'] = projeto.id  # Garantir que o comentário será associado ao projeto correto

        serializer = ComentarioProjetoSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ComentarioProjetoIdView(APIView):
    def delete(self, request, pk=None):
        """
        Exclui um comentário específico.
        """
        try:
            comentario = ComentarioProjeto.objects.get(pk=pk, autor=request.user)  # Verifique se o usuário é o autor do comentário
        except ComentarioProjeto.DoesNotExist:
            return Response({"detail": "Comentário não encontrado ou você não tem permissão para excluí-lo."},
                            status=status.HTTP_404_NOT_FOUND)

        comentario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ComentarioTarefaView(APIView):
    @swagger_auto_schema(
        operation_summary='Retorna os comentários de um tarefa.',
        responses={
            200: ComentarioTarefaSerializer(many=True),
            400: 'Tipo inválido, use "tarefa".',
            404: 'Projeto não encontrado.'
        }
    )
    def get(self, request, pk):
        """
        Retorna todos os comentários de um tarefa específico.
        """
        try:
            tarefa = Tarefas.objects.get(id=pk)
            comentarios = ComentarioTarefa.objects.filter(tarefa=tarefa)
        except Tarefas.DoesNotExist:
            return Response({"detail": "Tarefa não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ComentarioTarefaSerializer(comentarios, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Cria um novo comentário para um tarefa.',
        request_body=ComentarioTarefaSerializer,
        responses={
            201: ComentarioTarefaSerializer,
            400: 'Dados inválidos.',
            404: 'Tarefa não encontrado.'
        }
    )
    def post(self, request, pk=None):
        """
        Cria um novo comentário associado a um tarefa específico.
            """
        try:
            tarefa = Tarefas.objects.get(id=request.data['tarefa'])
            
        except Tarefas.DoesNotExist:
            return Response({"detail": "Tarefa não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if not tarefa:
            return Response({"detail": "Tarefa não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # Associando o tarefa ao comentário
        # request.data['tarefa'] = tarefa.id  # Garantir que o comentário será associado ao tarefa correto

        serializer = ComentarioTarefaSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ComentarioTarefaIdView(APIView):
    def delete(self, request, pk=None):
        """
        Exclui um comentário específico.
        """
        try:
            comentario = ComentarioTarefa.objects.get(pk=pk, autor=request.user)  # Verifique se o usuário é o autor do comentário
        except ComentarioTarefa.DoesNotExist:
            return Response({"detail": "Comentário não encontrado ou você não tem permissão para excluí-lo."},
                            status=status.HTTP_404_NOT_FOUND)

        comentario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ConviteView(APIView):
    @swagger_auto_schema(
        responses={
            200: ConviteSerializer(many=True),
            400: 'Tipo inválido, use "convite".',
            404: 'Convite não encontrado.'
        }
    )
    def get(self, request):
        convites = Convites.objects.filter(recebido_por=request.user)  # Filtra convites associados ao usuário

        serializer = ConviteSerializer(convites, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ConviteSerializer, responses={201: 'convite enviado'})
    def post(self, request):
        # Associar automaticamente o usuário autenticado ao projeto
        serializer = ConviteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Adiciona o usuário autenticado
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ConviteIdView(APIView):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
    ]

    @swagger_auto_schema(
    operation_summary='Arrumar os convites.',
    manual_parameters=[
        openapi.Parameter(
            name='status',
            in_=openapi.IN_QUERY,
            description='Status do convite.',
            type=openapi.TYPE_STRING,
            enum=[status[0] for status in STATUS_CHOICES]
        )
    ],
    responses={
        200: ConviteSerializer(many=True),
        400: 'Status inválido.',
        404: 'Nenhum projeto encontrado com o status especificado.'
    })
    def put(self, request, pk=None):
        """
        Atualiza o status de um convite baseado no ID.
        """
        # Buscar o convite pelo ID (pk)
        try:
            convite = Convites.objects.get(pk=pk)
        except Convites.DoesNotExist:
            return Response({"detail": "Convite não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Obter o novo status da query string
        novo_status = request.query_params.get('status')

        if novo_status and novo_status in dict(self.STATUS_CHOICES):
            convite.status = novo_status
            convite.save()  # Salva a alteração no banco de dados
            serializer = ConviteSerializer(convite)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Status inválido."}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(
        operation_summary='Deleta um convite pelo ID.',
        responses={
            204: 'Convite deletado com sucesso.',
            404: 'Convite não encontrado.'
        }
    )
    def delete(self, request, pk=None):
        """
        Deleta um convite baseado no ID.
        """
        try:
            convite = Convites.objects.get(pk=pk)
        except Convites.DoesNotExist:
            return Response({"detail": "Convite não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        convite.delete()  # Deleta o convite
        return Response({"detail": "Convite deletado com sucesso."}, status=status.HTTP_204_NO_CONTENT)
