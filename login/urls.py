from django.urls import path
from .views import UserView

urlpatterns = [
    path('users/', UserView.as_view(), name='user_list'),
    path('users/create/', UserView.as_view(), name='user_create'),
    path('users/<int:pk>/', UserView.as_view(), name='user_detail'),
]