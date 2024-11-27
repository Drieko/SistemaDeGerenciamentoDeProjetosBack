from django.urls import path
from .views import (ProjetoView, ProjetoIdView, ProjetoStatusView ,TarefaView, TarefaIdView, ComentarioProjetoView, 
                    ComentarioProjetoIdView, ComentarioTarefaView, ComentarioTarefaIdView, ConviteView, ConviteIdView)


urlpatterns = [
    #projetos
    path('projetos/', ProjetoView.as_view(), name='projeto_list'),
    path('projetos/<uuid:pk>/', ProjetoIdView.as_view(), name='projeto-detail'),
    path('projetos/status/', ProjetoStatusView.as_view(), name='projeto-status'),
    #tarefas
    path('tarefas/', TarefaView.as_view(), name='tarefas_list'),
    path('tarefas/<uuid:pk>/', TarefaIdView.as_view(), name='tarefas-detail'),
    #comentarios
    path('comentariosProjeto/<uuid:pk>/', ComentarioProjetoView.as_view(), name='comentarios_list'),
    path('comentariosProjeto/<uuid:pk>', ComentarioProjetoIdView.as_view(), name='comentarios-detail'),
    path('comentariosTarefa/<uuid:pk>/', ComentarioTarefaView.as_view(), name='comentarios_list'),
    path('comentarioTarefa/<uuid:pk>', ComentarioTarefaIdView.as_view(), name='comentarios-detail'),
    #convites
    path('convites/', ConviteView.as_view(), name= 'convites'),
    path('convites/<uuid:pk>/', ConviteIdView.as_view(), name='convites-detail')
    ]




