from rest_framework import serializers

from .models import ToDo, TimeSeries, Dates, Delta, Delta7, Total, CRDTV


class ToDoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'


class CRDTVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CRDTV
        fields = '__all__'



class DeltaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Delta
        fields = ('delta',)


class Delta7Serializer(serializers.ModelSerializer):

    class Meta:
        model = Delta7
        fields = ('delta7',)


class TotalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Total
        fields = ('total',)


class DatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dates
        fields = ('date', 'total', 'delta', 'delta7')
        depth = 2


class StatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeSeries
        fields = ('dates', 'state')
        depth = 3
