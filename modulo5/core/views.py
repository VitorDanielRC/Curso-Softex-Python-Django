from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from django.utils import timezone
from .models import Tarefa
from .serializers import TarefaSerializer
from rest_framework.decorators import action
from django.db import transaction


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
        
        
class DetalheTarefaAPIView(APIView):
    def get_object(self, pk):
        """
        Busca a tarefa pelo ID e retorna 404 se não encontrada.
        """
        return get_object_or_404(Tarefa, pk=pk)
    
    def get(self, request, pk, format=None):
        """
        Retorna os dados de uma tarefa específica.
        Args:
        pk: ID da tarefa na URL
        Returns:
        200 OK: Tarefa encontrada
        404 Not Found: Tarefa não existe
        """
        # 1. BUSCAR: Usa método auxiliar (trata 404)
        tarefa = self.get_object(pk)
        # 2. SERIALIZAR: Converte objeto único (sem many=True)
        serializer = TarefaSerializer(tarefa)
        # 3. RESPONDER: Retorna JSON com status 200
        return Response(serializer.data, status=status.HTTP_200_OK)
    def put(self, request, pk, format=None):
        """
        Atualiza tarefa completamente (substituição total).
        Exige que TODOS os campos editáveis sejam enviados.
        """
        # 1. BUSCAR: Obter o objeto existente
        tarefa = self.get_object(pk)
        # 2. SERIALIZAR: Passar objeto antigo E novos dados
        serializer = TarefaSerializer(tarefa, data=request.data)
        # ^^^^^ ^^^^^^^^^^^^^^^^
        # | Nova versão
        # Versão atual
        # 3. VALIDAR: Checar se JSON está completo e válido
        if serializer.is_valid():
        # 4. SALVAR: Atualizar no banco
            serializer.save()
        # 5. RESPONDER: Retornar objeto atualizado
            return Response(serializer.data, status=status.HTTP_200_OK)
        # ERRO: Retornar erros de validação
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk, format=None):
        """
        Atualiza tarefa parcialmente (merge).
        Permite enviar apenas os campos que serão modificados.
        """
    # 1. BUSCAR: Obter o objeto existente
        tarefa = self.get_object(pk)
    # 2. SERIALIZAR: Passar objeto, novos dados E partial=True
        serializer = TarefaSerializer(
        tarefa,
        data=request.data,
        partial=True # <--- ESSENCIAL PARA O PATCH
        )
    # 3. VALIDAR
        if serializer.is_valid():
    # 4. SALVAR (aplica apenas os campos recebidos)
            serializer.save()
    # 5. RESPONDER
            return Response(serializer.data, status=status.HTTP_200_OK)
    # ERRO
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        """
        Remove um recurso específico.
        """
        # 1. BUSCAR: Obter o objeto (trata 404 se não existir)
        tarefa = self.get_object(pk)
        # 2. DELETAR
        tarefa.delete()
        # 3. RESPONDER: 204 No Content (sucesso sem corpo de resposta)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TarefaViewSet(viewsets.ModelViewSet):
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
    
    @action(detail=True, methods=["post"], url_path="duplicar")
    def duplicar(self, request, pk=None):
        original = self.get_object()
        
        copia.concluida = False
        copia.conclusao = None
        
        if hasattr(copia, "titulo") and copia.titulo:
            copia.titulo = f"{copia.titulo} (copia)"
            
        copia.save()
        
        serializer = self.get_serializer(copia)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    @action(detail=False, methods=["patch"], url_path="concluir-todas")
    def concluir_todas(self, request):
        qs = self.get_queryset().filter(concluida=False).exclude(prioridade="alta")
        
        agora = timezone.now()
        
        with transaction.atomic():
            atualizadas = qs.update(concluida=True, data_conclusao=agora)
            
            return Response(
                {"mensagem":"Tarefas concluidas (exceto alta prioridade).", "atualizadas":atualizadas},
                status=status.HTTP_200_OK
            )