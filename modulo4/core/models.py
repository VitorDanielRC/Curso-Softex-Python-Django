from django.db import models
from django.contrib.auth.models import User
class Tarefa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length= 200)
    concluida = models.BooleanField(default= False)
    criada_em = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.titulo


class execucao(models.Model):
    nome = models.CharField(max_length= 200)
    local = models.CharField(max_length= 200)
    hora = models.DateTimeField(auto_now_add= True)
    concluida = models.BooleanField(default = False)

    def __str__(self):
        return self.nome