from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# envolvendo projetos
from .models import Projetos
from .serializers import ProjetoSerializer

#envolvendo tarefas
from .models import Tarefas
from .serializers import TarefaSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

#projetos
class ProjetoView(APIView):
    @swagger_auto_schema(responses={200: 'Lista de projetos'})
    def get(self, request):
        projetos = Projetos.objects.all()
        serializer = ProjetoSerializer(projetos, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=ProjetoSerializer, responses={201: 'Projeto criado'})
    def post(self, request):
        serializer = ProjetoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#VER DEPOIS DELETE DEU RUIM !!!!!!!!!!!!!!!!!!!!!
    # @swagger_auto_schema(request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             'id': openapi.Schema(type=openapi.TYPE_STRING,   format=openapi.FORMAT_UUID,  description='ID do projeto a ser deletado')
    #         },
    #         required=['id']
    #     ),
    #     responses={204: 'Projeto deletado'}
    # )
    # def delete(self, request):
    #     serializer = ProjetoSerializer(data=request.data.get('id'))
    #     if serializer.is_valid():
    #         try:
    #             projeto = Projetos.objects.get(id=projeto_id)
    #             projeto.delete()
    #             return Response({"message": "Projeto deletado com sucesso."}, status=status.    HTTP_204_NO_CONTENT)
    #         except Projetos.DoesNotExist:
    #             return Response({"error": "Projeto não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    #             projeto_id = serializer.validated_data['id']
    #             projeto = get_object_or_404(Projetos, id=projeto_id)
    #             projeto.delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


    
