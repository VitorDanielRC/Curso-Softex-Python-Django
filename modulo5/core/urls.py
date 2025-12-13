from django.urls import path
from .views import (ListaTarefasAPIView, TarefaEstatisticasAPIView, TarefaSoftDeleteAPIView, DetalheTarefaAPIView)
from rest_framework.routers import DefaultRouter
from .views import TarefaViewSet

app_name = 'core'
urlpatterns = [
    path('tarefas/', ListaTarefasAPIView.as_view(), name='lista-tarefas'),
    path('tarefas/estatisticas/', TarefaEstatisticasAPIView.as_view(), name='tarefas-estatisticas'),
    path('tarefas/<int:pk>/soft_delete/', TarefaSoftDeleteAPIView.as_view(), name='tarefa-soft-delete'),
    path('tarefas/<int:pk>/',DetalheTarefaAPIView.as_view(),name='detalhe-tarefa'),
]


router = DefaultRouter()
router.register(r"tarefas", TarefaViewSet, basename="tarefas")

urlpatterns = router.urls