from django.urls import path
from .views import ProjetoView

urlpatterns = [
    path('', ProjetoView.as_view(), name='user_list'),
]