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
        ('andamento', ('Em andamento')),
        ('cancelado', ('Cancelado')),
        ('concluido', ('Concluído')),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='andamento')

    def __str__(self):
        
        return f"{self.titulo} - {self.description} - {self.prazo} - {self.created}"

class Tarefas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #pegar a foreign key do projeto em questão
    projeto = models.ForeignKey(Projetos, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    prazo = models.DateField(null=True, blank=True)

    PRIORIDADE_CHOICES = [
    ('baixa', ('Baixa')),
    ('media', ('Média')),
    ('alta', ('Alta')),
    ]
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='media')
    
