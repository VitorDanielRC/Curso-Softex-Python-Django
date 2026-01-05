# core/tests/test_serializers.py
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Tarefa
from core.serializers import TarefaSerializer
class TarefaSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
        username='testuser',
        password='testpass123'
        )
        self.tarefa_data = {
        'titulo': 'Tarefa Serializada',
        'concluida': False
    # Note que 'user' não entra aqui, pois geralmente vem do request context
    }
    def test_serializer_com_dados_validos(self):
        """Testa se o serializer aceita dados corretos."""
        serializer = TarefaSerializer(data=self.tarefa_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['titulo'], 'Tarefa Serializada')
    def test_serializer_sem_titulo(self):
        """Testa se o campo obrigatório 'titulo' é validado."""
        dados_invalidos = {'concluida': False}
        serializer = TarefaSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        # Verifica se a chave do erro é exatamente 'titulo'
        self.assertIn('titulo', serializer.errors)
    def test_serializer_titulo_muito_longo(self):
        """Testa validação de max_length (ex: 200 caracteres)."""
        dados_invalidos = {
        'titulo': 'a' * 201, # Cria string com 201 caracteres
        'concluida': False
        }
        serializer = TarefaSerializer(data=dados_invalidos)
        self.assertFalse(serializer.is_valid())
        self.assertIn('titulo', serializer.errors)
    def test_desserializacao_output(self):
        """Testa se a conversão de Objeto Python -> JSON está correta."""
        tarefa = Tarefa.objects.create(
        user=self.user,
        titulo='Tarefa Existente',
        concluida=True
        )
        serializer = TarefaSerializer(tarefa)
        data = serializer.data
        self.assertEqual(data['titulo'], 'Tarefa Existente')
        self.assertTrue(data['concluida'])
        self.assertEqual(data['id'], tarefa.id)