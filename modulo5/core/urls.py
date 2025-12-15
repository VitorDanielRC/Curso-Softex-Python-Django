from django.urls import path
from .views import (ListaTarefasAPIView, TarefaEstatisticasAPIView, TarefaSoftDeleteAPIView, DetalheTarefaAPIView)
from rest_framework.routers import DefaultRouter
from .views import TarefaViewSet
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


app_name = 'core'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('api/', include('core.urls')),
    path('tarefas/', ListaTarefasAPIView.as_view(), name='lista-tarefas'),
    path('tarefas/estatisticas/', TarefaEstatisticasAPIView.as_view(), name='tarefas-estatisticas'),
    path('tarefas/<int:pk>/soft_delete/', TarefaSoftDeleteAPIView.as_view(), name='tarefa-soft-delete'),
    path('tarefas/<int:pk>/',DetalheTarefaAPIView.as_view(),name='detalhe-tarefa'),
]


router = DefaultRouter()
router.register(r"tarefas", TarefaViewSet, basename="tarefas")

urlpatterns = router.urls