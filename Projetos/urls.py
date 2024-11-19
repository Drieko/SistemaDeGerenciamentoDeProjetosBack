from django.urls import path
from .views import ProjetoView, ProjetoIdView, TarefaView, TarefaIdView, ComentarioView, ComentarioIdView


urlpatterns = [
    path('projetos/', ProjetoView.as_view(), name='projeto_list'),
    path('projetos/<uuid:pk>/', ProjetoIdView.as_view(), name='projeto-detail'),
    path('tarefas/', TarefaView.as_view(), name='tarefas_list'),
    path('tarefas/<uuid:pk>/', TarefaIdView.as_view(), name='tarefas-detail'),
    path('comentarios/', ComentarioView.as_view(), name='comentarios_list'),
    path('comentarios/<uuid:pk>', ComentarioIdView.as_view(), name='comentarios-detail')
    ]




