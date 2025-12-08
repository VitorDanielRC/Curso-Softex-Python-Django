from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from .models import Tarefa 
from .serializers import TarefaSerializer 
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
import logging
logger = logging.getLogger(__name__)

class ListaTarefasAPIView(APIView): 
    """ 
    View para listar todas as tarefas (GET). 
     
    Endpoints: 
        GET /api/tarefas/ - Lista todas as tarefas 
    """ 
     
    def get(self, request, format=None): 
        """ 
        Retorna lista de todas as tarefas do banco. 
         
        Returns: 
            Response: JSON com lista de tarefas e status 200 
        """ 
        # 1. BUSCAR: ORM do Django busca todos os registros 
        tarefas = Tarefa.objects.all() 
         
        # 2. SERIALIZAR: Converter objetos Python → JSON 
        # many=True: indica que é uma lista de objetos 
        serializer = TarefaSerializer(tarefas, many=True) 
         
        # 3. RESPONDER: Retornar JSON com status HTTP 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        """
        Cria uma nova tarefa.
        Args:
            request.data: JSON com dados da tarefa
                {
                    "titulo": "string",
                    "concluida": boolean (opcional, default=False)
                }
        Returns:
            201 Created: Tarefa criada com sucesso
            400 Bad Request: Dados inválidos
        """
        # 1. INSTANCIAR: Criar serializer com dados recebidos
        serializer = TarefaSerializer(data=request.data)
        # 2. VALIDAR: Checar se os dados são válidos
        if serializer.is_valid():
            # 3. SALVAR: Persistir no banco de dados
            serializer.save()
            # 4. RESPONDER: Retornar objeto criado + status 201
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        # 5. ERRO: Retornar erros de validação + status 400
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
