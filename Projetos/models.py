from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid


class Projetos(models.Model):
    #tupla de opções pro campo status 
    STATUS_CHOICES = [
        ('andamento', ('Em andamento')),
        ('cancelado', ('Cancelado')),
        ('concluido', ('Concluído')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    prazo = models.DateField(null=True, blank=True)
    usuarios = models.ManyToManyField(User, related_name='projetos', blank=True)
    
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

    CONCLUIDA_CHOICES = [
        (True, 'Sim'),
        (False, 'Não')
    ]
    concluida = models.BooleanField(choices=CONCLUIDA_CHOICES, default=False)

    def __str__(self):
        return f"{self.titulo} - {self.description} - {self.prazo} - {self.created}"

class ComentarioProjeto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # O autor do comentário
    texto = models.TextField()  # O conteúdo do comentário
    data_criacao = models.DateTimeField(default=timezone.now)  # Data e hora de criação do comentário
    projeto = models.ForeignKey('Projetos', on_delete=models.CASCADE, null=True, blank=True, related_name='comentarios')  # Relacionamento com o Projeto

    def __str__(self):
        return f"Comentário de {self.autor} em {self.data_criacao}"

    class Meta:
        ordering = ['data_criacao']  # Ordena os comentários pela data de criação

class ComentarioTarefa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)  # O autor do comentário
    texto = models.TextField()  # O conteúdo do comentário
    data_criacao = models.DateTimeField(default=timezone.now)  # Data e hora de criação do comentário
    tarefa = models.ForeignKey('Tarefas', on_delete=models.CASCADE, null=True, blank=True, related_name='comentarios')  # Relacionamento com a Tarefa

    def __str__(self):
        return f"Comentário de {self.autor} em {self.data_criacao}"

    class Meta:
        ordering = ['data_criacao']  # Ordena os comentários pela data de criação


class Convites(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aceito', 'Aceito'),
        ('recusado', 'Recusado'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')

    # Campos do modelo
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enviado_por = models.ForeignKey(User, related_name='convites_enviados', on_delete=models.CASCADE)
    recebido_por = models.ForeignKey(User, related_name='convites_recebidos', on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projetos, on_delete=models.CASCADE)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Convite de {self.enviado_por} para {self.recebido_por} no projeto {self.projeto.nome} - Status: {self.status}"