from django.urls import path
from .views import ProjetoView, ProjetoIdView,TarefaView


urlpatterns = [
    path('projetos/', ProjetoView.as_view(), name='projeto_list'),
    path('projetos/<uuid:pk>/', ProjetoIdView.as_view(), name='projeto-detail'),
    path('tarefas/', TarefaView.as_view(), name='user_list'),
]




