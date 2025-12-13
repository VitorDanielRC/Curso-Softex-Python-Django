from rest_framework import serializers
from .models import Tarefa
from datetime import date
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class TarefaSerializer(serializers.ModelSerializer):
    """
    Serializer para o Model Tarefa.
    Responsabilidades:
    1. Converter Tarefa → JSON (serialização)
    2. Converter JSON → Tarefa (desserialização)
    3. Validar dados de entrada
    """
    titulo = serializers.CharField(
        max_length=200,
        error_messages={
        'required': 'O título é obrigatório.',
        'blank': 'O título não pode ser vazio.',
        'max_length': 'O título não pode ter mais de 200 caracteres.'
        }
    )

    class Meta:
        model = Tarefa
        fields = ['id', 'user', 'titulo', 'concluida', 'prioridade', 'prazo', 'deletada', 'criada_em', 'Data_conclusao']
        # Campos gerados automaticamente (não aceitos na entrada)
        read_only_fields = ['id', 'user', 'deletada','criada_em']
    def validate_titulo(self, value):
        """
                Validação customizada para o campo 'titulo'.

                Regras:
                - Não pode ser vazio (após strip)
                - Não pode conter apenas números
                - Deve ter pelo menos 3 caracteres
        """
        # Remover espaços em branco
        value = value.strip()

        # Validação 1: Não vazio
        if not value:
            raise serializers.ValidationError(
        "O título não pode ser vazio ou conter apenas espaços."
        )

        # Validação 2: Mínimo de caracteres
        if len(value) < 3:
            raise serializers.ValidationError(
        "O título deve ter pelo menos 3 caracteres."
        )

        # Validação 3: Não apenas números
        if value.isdigit():
            raise serializers.ValidationError(
        "O título não pode conter apenas números."
        )
        

        return value
    
    def validate_prioridade(self, value):
        valores = [choice[0] for choice in Tarefa.PRIORIDADE_CHOICES]
        if value not in valores:
            raise serializers.ValidationError("Prioridade Invalida.")
        return value
    def validate(self, attrs):
        prazo = attrs.get('prazo',getattr(self.instance, 'prazo', None))
        concluida = attrs.get('concluida', getattr(self.instance, 'concluida', False))
        
        
        if not concluida and prazo is None:
            raise serializers.ValidationError({
                'prazo' : 'Prazo e obrigatorio'
            })
            
        if prazo is not None and prazo < date.today():
            raise serializers.ValidationError({
                'prazo' : 'Prazo nao pode ser no passado'
                })
        return attrs
    
    class TarefasSeri(serializers.ModelSerializer):
        class Meta:
            model = Tarefa
            fields = "_all_"
        
        def conclusao(self, attrs, instance = None):
            concluida_final = attrs.get("concluida", getattr(instance, "concluida", False))
            
            if concluida_final is True:
                if attrs.get("data_conclusao") is None:
                    attrs["data_conclusao"] = None
                
                return attrs
            
            def create(self, validaçao_data):
                validaçao_data = self.conclusao(validaçao_data, instance = instance)
                return super().update(instance, validaçao_data)
            
        
class validacao(serializers.ModelSerializer):
    def validate(self, attrs):
        request = self.context.get("request")
        method = getattr(request, "method", "").upper()
        
        instance = getattr(self, "instance", None)
        prioridade_final = attrs.get("prioridade", getattr(instance, "prioridade", None))
        concluida_final = attrs.get("concluida", getattr(instance, "concluida", False))
        
        if prioridade_final == "alta" and concluida_final is True and method != "PUT":
            raise ValidationError({
                "concluida":"Tarefas de alta Prioridade"
            })
        return attrs