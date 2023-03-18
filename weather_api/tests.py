from django.urls import reverse
from rest_framework.test import APITestCase
from weather_api.models import Weather, WeatherStats
from weather_api.service import feed_data_to_model, data_analysis_of_weather

class DataMigrationTest(APITestCase):

    def setup(self):
        pass

    def test_data_migration_and_data_analysis(self):
        feed_data_to_model('test_data')
        self.assertTrue(Weather.objects.all().exists())

        data_analysis_of_weather()
        self.assertTrue(WeatherStats.objects.all().exists())

    def test_weather_list_api(self):
        # migrate dataset to database
        feed_data_to_model('test_data')
        data_analysis_of_weather()
        # normal API test
        url = reverse('weather-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 8+4) # 8 from first test dataset and 4 from second test dataset

        # API testing with wrong station_id  filter
        filter_url = f'{url}?station_id=123'
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 0)

        # API testing with appropriate station_id filter
        filter_url = f'{url}?station_id=USC0001'
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 8)

        # API testing with appropriate date filter
        filter_url = f'{url}?date=1985-01-08'
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['count'], 1)

    def test_weather_stats_api(self):
        # migrate dataset to database
        feed_data_to_model('test_data')
        data_analysis_of_weather()

        # normal API testing
        url = reverse('weather-stats')
        self.assert_values_and_check_status_code(url, 2)

        # API testing with wrong station_id  filter
        filter_url = f'{url}?station_id=123'
        self.assert_values_and_check_status_code(filter_url, 0)

        # API testing with appropriate station_id filter
        filter_url = f'{url}?station_id=USC0001'
        response = self.assert_values_and_check_status_code(filter_url, 1)

        # API testing with appropriate year filter
        filter_url = f'{url}?year=1985'
        response = self.assert_values_and_check_status_code(filter_url, 2)

        # maximum_temperature_data from test dataset = -22, -122, -106, -56, 11, 28, 22, -6
        filter_url = f'{url}?station_id=USC0001'
        self.assertEqual(response.json()['results'][0]['average_maximum_temperature'], -31.38)

    def assert_values_and_check_status_code(self, url, count):
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()['count'], count)

        return result
        