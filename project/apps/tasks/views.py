from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from tasks.filters import TaskFilter
from tasks.models import Task
from tasks.serializers import TaskSerializer, TaskCreateSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all().order_by('-priority')
    permission_classes = [IsAuthenticated]
    filterset_class = TaskFilter

    def get_serializer_class(self):
        serializer_class = TaskSerializer

        if self.action in ['create', 'update', 'partial_update']:
            serializer_class = TaskCreateSerializer

        return serializer_class

