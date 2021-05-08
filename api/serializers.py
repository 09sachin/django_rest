from rest_framework import serializers

from .models import ToDo


class ToDoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ToDo
        fields = ('id','name', 'details','created_at','updated_at')
