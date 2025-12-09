from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q

from .models import Tarefa
from .serializers import TarefaSerializer


class ListaTarefasAPIView(APIView):
    """
    Endpoint:
        GET  /api/tarefas/   -> lista tarefas do usuário logado (não deletadas)
        POST /api/tarefas/   -> cria nova tarefa para o usuário logado
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Retorna lista de todas as tarefas do usuário logado
        que NÃO estão marcadas como deletadas.
        """
        tarefas = Tarefa.objects.filter(
            user=request.user,
            deletada=False
        )
        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Cria uma nova tarefa.

        Exemplo de corpo:
        {
            "titulo": "Estudar Django",
            "concluida": false,
            "prioridade": "media",
            "prazo": "2025-01-20"
        }
        """
        serializer = TarefaSerializer(data=request.data)
        if serializer.is_valid():
            # Vincula a tarefa ao usuário autenticado
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TarefaEstatisticasAPIView(APIView):
    """
    Endpoint:
        GET /api/tarefas/estatisticas/

    Retorna:
    {
        "total": 10,
        "concluidas": 6,
        "pendentes": 4,
        "taxa_conclusao": 0.6
    }
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Considera apenas tarefas do usuário e não deletadas
        qs = Tarefa.objects.filter(
            user=request.user,
            deletada=False
        )

        dados = qs.aggregate(
            total=Count('id'),
            concluidas=Count('id', filter=Q(concluida=True)),
        )

        total = dados['total'] or 0
        concluidas = dados['concluidas'] or 0
        pendentes = total - concluidas
        taxa_conclusao = concluidas / total if total > 0 else 0

        return Response(
            {
                "total": total,
                "concluidas": concluidas,
                "pendentes": pendentes,
                "taxa_conclusao": taxa_conclusao,
            },
            status=status.HTTP_200_OK
        )


class TarefaSoftDeleteAPIView(APIView):
    """
    Endpoint:
        PATCH /api/tarefas/<pk>/soft_delete/

    Marca uma tarefa como deletada sem remover do banco.
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        tarefa = get_object_or_404(
            Tarefa,
            pk=pk,
            user=request.user,
            deletada=False
        )

        tarefa.deletada = True
        tarefa.save()

        return Response(
            {"detail": "Tarefa marcada como deletada."},
            status=status.HTTP_200_OK
        )
