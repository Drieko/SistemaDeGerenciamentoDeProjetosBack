from django.urls import path
from .views import ProjetoView, TarefaView


urlpatterns = [
    path('', ProjetoView.as_view(), name='Projeto_list'),
    path('tarefas/', TarefaView.as_view(), name='user_list'),
]




