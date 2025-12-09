from django.urls import path
from .views import (ListaTarefasAPIView, TarefaEstatisticasAPIView, TarefaSoftDeleteAPIView)

app_name = 'core'
urlpatterns = [
    path('tarefas/', ListaTarefasAPIView.as_view(), name='lista-tarefas'),
    path('tarefas/estatisticas/', TarefaEstatisticasAPIView.as_view(), name='tarefas-estatisticas'),
    path('tarefas/<int:pk>/soft_delete/', TarefaSoftDeleteAPIView.as_view(), name='tarefa-soft-delete'),
    
]
