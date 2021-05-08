from rest_framework import viewsets

from .serializers import ToDoSerializer
from .models import ToDo


class ToDoViewSet(viewsets.ModelViewSet):
    queryset = ToDo.objects.all().order_by('name')
    serializer_class = ToDoSerializer