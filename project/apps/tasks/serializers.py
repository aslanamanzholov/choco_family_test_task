from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    priority_name = serializers.CharField(source='get_priority_display')

    class Meta:
        model = Task
        fields = [
            'uuid',
            'name',
            'priority',
            'priority_name',
            'end_date',
            'status'
        ]
        read_only_fields = fields


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'uuid',
            'name',
            'priority',
            'end_date',
            'status'
        ]
        read_only_fields = ('uuid',)
