from rest_framework import serializers
from .models import Resume


class ResumeListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка резюме (только id и базовая информация)"""

    class Meta:
        model = Resume
        fields = ['id', 'applicant_name', 'position', 'status', 'created_at']


class ResumeStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления статуса"""

    class Meta:
        model = Resume
        fields = ['id', 'status']
        read_only_fields = ['id']