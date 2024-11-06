from django.db import models

# Create your models here.
class User(models.Model):
    nome = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=30)

def __str__(self):
    return f"{self.nome} ({self.email})"