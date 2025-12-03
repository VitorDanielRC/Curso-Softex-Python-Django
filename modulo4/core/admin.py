from django.contrib import admin
from .models import Tarefa

class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'user', 'concluida', 'criada_em')
    list_filter = ('concluida', 'user', 'criada_em')
    search_fields = ('titulo', 'user__username')
    fieldsets = (
('Informações Principais', {
'fields': ('user', 'titulo')
}),
('Status da Tarefa', {
'fields': ('concluida', 'criada_em')
}),
)
# 'readonly_fields' define campos que podem ser vistos, mas não editados
# Perfeito para campos automáticos como 'criada_em'
readonly_fields = ('criada_em',)

@admin.display(description='Email do Usuário') # Define o título da coluna
def get_user_email(self, obj):
    return obj.user.email
admin.site.register(Tarefa, TarefaAdmin)

# Register your models here.
