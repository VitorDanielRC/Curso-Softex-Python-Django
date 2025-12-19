from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tarefa
from .serializers import TarefaSerializer, UserProfileSerializer
from django.db import IntegrityError
import logging
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveAPIView
from .permissions import IsAdminOrOwner

logger = logging.getLogger(__name__)


class ListaTarefasAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        if request.user.is_staff:
            tarefas = Tarefa.objects.all()
        else:
            tarefas = Tarefa.objects.filter(user=request.user)

        serializer = TarefaSerializer(tarefas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            serializer = TarefaSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                logger.info(f"Tarefa criada: {serializer.data.get('id')}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IntegrityError:
            return Response(
                {'error': 'Violação de integridade no banco de dados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return Response(
                {'error': 'Erro interno do servidor.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DetalheTarefaAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get_object(self, request, pk):
        tarefa = get_object_or_404(Tarefa, pk=pk)
        self.check_object_permissions(request, tarefa)
        return tarefa

    def get(self, request, pk, format=None):
        tarefa = self.get_object(request, pk)
        serializer = TarefaSerializer(tarefa)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        tarefa = self.get_object(request, pk)
        serializer = TarefaSerializer(tarefa, data=request.data)

        if serializer.is_valid():
            serializer.save(user=tarefa.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        tarefa = self.get_object(request, pk)
        serializer = TarefaSerializer(tarefa, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(user=tarefa.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        tarefa = self.get_object(request, pk)
        tarefa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TarefasEstatisticasAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        tarefas = Tarefa.objects.filter(user=request.user)

        total = tarefas.count()
        concluidas = tarefas.filter(concluida=True).count()
        pendentes = total - concluidas
        taxa_conclusao = concluidas / total if total > 0 else 0

        return Response({
            "total": total,
            "concluidas": concluidas,
            "pendentes": pendentes,
            "taxa_conclusao": round(taxa_conclusao, 2)
        }, status=status.HTTP_200_OK)


class MinhaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            f"Usuário autenticado: {request.user.username}",
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response(
                    {"detail": "Refresh token não enviado."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {"detail": "Logout realizado com sucesso."},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {"detail": "Token inválido."},
                status=status.HTTP_400_BAD_REQUEST
            )


class MeView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {"error": "old_password e new_password são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "Senha atual incorreta"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"detail": "Senha alterada com sucesso"},
            status=status.HTTP_200_OK
        )


class StatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tarefas = Tarefa.objects.filter(user=request.user)

        total = tarefas.count()
        concluidas = tarefas.filter(concluida=True).count()
        pendentes = total - concluidas
        taxa_conclusao = concluidas / total if total > 0 else 0

        return Response({
            "total_tarefas": total,
            "concluidas": concluidas,
            "pendentes": pendentes,
            "taxa_conclusao": round(taxa_conclusao, 2)
        }, status=status.HTTP_200_OK)
