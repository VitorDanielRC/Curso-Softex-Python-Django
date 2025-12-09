from django.db import models
from django.contrib.auth.models import User

class Tarefa(models.Model):
    PRIORIDADE_CHOICES = [
    ('baixa', 'Baixa'),
    ('media', 'Média'),
    ('alta', 'Alta'),
    ]


    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='tarefas',
    verbose_name='Usuário'
    )

    titulo = models.CharField(
    max_length=200,
    verbose_name='Título'
    )
    
    concluida = models.BooleanField(
    default=False,
    verbose_name='Concluída'
    )
    
    prioridade = models.CharField(
    max_length=10,
    choices=PRIORIDADE_CHOICES,
    default='media'
    )
    
    prazo = models.DateField(
        null=True,
        blank=True,
        verbose_name='Prazo'
    )
    
    deletada = models.BooleanField(
        default=False,
        verbose_name='Deletada'
    )
    
    criada_em = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Criada em'
    )

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['-criada_em'] 
        
    def __str__(self):
        """Representação em string (usado no admin)"""
        return f"{self.titulo} ({'✓' if self.concluida else '✗'})"