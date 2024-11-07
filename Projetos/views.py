from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Projetos
from .serializers import ProjetoSerializer
from drf_yasg.utils import swagger_auto_schema

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
    