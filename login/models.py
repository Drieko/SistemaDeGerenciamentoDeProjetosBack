from django.contrib.auth.hashers import check_password
from django.db import models

# Create your models here.
class User(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=30)
    def check_password(self, password):
        return check_password(password, self.senha)
    def __str__(self):
        return f"{self.nome} ({self.email})"   