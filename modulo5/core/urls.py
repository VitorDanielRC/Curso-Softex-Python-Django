from django.urls import path
from .views import (
    ListaTarefasAPIView,
    DetalheTarefaAPIView,
    TarefasEstatisticasAPIView,
    MinhaView,
    LogoutView,
    MeView,
    ChangePasswordView,
    StatsView,
)

app_name = 'core'

urlpatterns = [
    path('tarefas/', ListaTarefasAPIView.as_view(), name='lista-tarefas'),
    path('tarefas/<int:pk>/', DetalheTarefaAPIView.as_view(), name='detalhe-tarefa'),
    path('teste/', MinhaView.as_view(), name='teste-autenticado'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('stats/', StatsView.as_view(), name='stats'),
]
