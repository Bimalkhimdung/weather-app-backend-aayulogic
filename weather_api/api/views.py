from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from weather_api.models import Weather, WeatherStats


class WeatherListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = '__all__'
        

class WeatherListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''Available filters

    station_id, date (format=YYYY-MM-DD)
    '''
    queryset = Weather.objects.all()
    serializer_class = WeatherListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station_id', 'date']
    permission_class = []


class WeatherStatsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStats
        fields = '__all__'
        

class WeatherStatsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''Available filters

    station_id, year
    '''
    queryset = WeatherStats.objects.all()
    serializer_class = WeatherStatsListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['station_id', 'year']
    permission_class = []

