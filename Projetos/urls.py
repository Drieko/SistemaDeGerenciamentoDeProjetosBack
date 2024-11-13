from django.urls import path
from .views import ProjetoView
from .views import TarefaView

urlpatterns = [
    path('', ProjetoView.as_view(), name='user_list'),
    path('tarefas/', TarefaView.as_view(), name='user_list'),
]

