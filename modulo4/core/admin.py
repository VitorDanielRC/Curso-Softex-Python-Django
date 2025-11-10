from django.contrib import admin
from .models import Tarefa
from .models import execucao
# Register your models here.
admin.site.register(Tarefa)
admin.site.register(execucao)