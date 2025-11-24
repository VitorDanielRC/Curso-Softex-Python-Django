from django.contrib import admin
from .models import Tarefa

class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'user', 'concluida', 'criada_em')
    list_filter = ('concluida', 'user', 'criada_em')
admin.site.register(Tarefa, TarefaAdmin)

# Register your models here.
