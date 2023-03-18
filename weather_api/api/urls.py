from django.urls import path, include

from weather_api.api.views import WeatherListViewSet, WeatherStatsListViewSet

urlpatterns = [
    path('stats/', WeatherStatsListViewSet.as_view({'get': 'list'}), name="weather-stats"),
    path('', WeatherListViewSet.as_view({'get': 'list'}), name="weather-stats"),
]