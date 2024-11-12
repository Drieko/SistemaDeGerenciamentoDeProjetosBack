from django.urls import path
from .views import UserCreateView

urlpatterns = [
    path('novo/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserCreateView.LoginView.as_view(), name='login'),
]
