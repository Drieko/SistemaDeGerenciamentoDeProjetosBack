from django.db import models
import uuid

class Projetos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    prazo = models.DateField(null=True, blank=True)

    #tupla de opções pro campo status 
    STATUS_CHOICES = [
        ('andamento', 'cancelado', 'concluido')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='andamento')

    def __str__(self):
        
        return f"{self.titulo} - {self.description} - {self.prazo} - {self.created}"