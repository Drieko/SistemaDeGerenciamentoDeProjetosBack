# login/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializer import UserSerializer
from .models import User

class UserView(APIView):
    @swagger_auto_schema(responses={200: 'Lista de usuários'})
    def get(self, request):
        usuarios = User.objects.all()
        serializer = UserSerializer(usuarios, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer, responses={201: 'Usuário criado'})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    