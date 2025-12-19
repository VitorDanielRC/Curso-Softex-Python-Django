from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Tarefa


class TarefaSerializer(serializers.ModelSerializer):

    titulo = serializers.CharField(
        max_length=200,
        error_messages={
            'required': 'O título é obrigatório.',
            'blank': 'O título não pode ser vazio.',
            'max_length': 'O título não pode ter mais de 200 caracteres.'
        }
    )

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Tarefa
        fields = [
            'id',
            'user',
            'titulo',
            'concluida',
            'prioridade',
            'prazo',
            'criada_em'
        ]
        read_only_fields = ['id', 'user', 'criada_em']

    def validate_titulo(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "O título não pode ser vazio ou conter apenas espaços."
            )
        if len(value) < 3:
            raise serializers.ValidationError(
                "O título deve ter pelo menos 3 caracteres."
            )
        if value.isdigit():
            raise serializers.ValidationError(
                "O título não pode conter apenas números."
            )

        return value

    def validate_prazo(self, value):
        if value is None:
            return value

        hoje = timezone.localdate()
        if value < hoje:
            raise serializers.ValidationError(
                "O prazo não pode ser uma data no passado."
            )

        return value


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        ]
        read_only_fields = ['id', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    grupos = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    cargo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'grupos',
            'cargo'
        ]

    def get_cargo(self, obj):
        grupo = obj.groups.first()
        return grupo.name if grupo else None
