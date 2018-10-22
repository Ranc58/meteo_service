import json
from datetime import datetime, timedelta


from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ForecastFactory
from .models import Forecast


class TestForecastsHandler(APITestCase):

    def setUp(self):
        self.base_url = '/a/v1/forecast'

    def create_test_data(self, days):
        for forecast_day in range(days):
            day = datetime.now().replace(hour=0) + timedelta(days=forecast_day)
            for forecast_hour in range(0, 24, 6):
                ForecastFactory(
                    forecast_datetime=day.replace(hour=forecast_hour)
                )

    def test_get_3_days_forecast_celsius(self):
        self.create_test_data(3)
        response = self.client.get(self.base_url)
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 12)
        self.assertEqual(data['type'], 'c')

    def test_get_5_days_forecast_celsius(self):
        self.create_test_data(5)
        response = self.client.get(self.base_url, {'days': 5})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 20)
        self.assertEqual(data['type'], 'c')

    def test_get_7_days_forecast_celsius(self):
        self.create_test_data(7)
        response = self.client.get(self.base_url, {'days': 7})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 28)
        self.assertEqual(data['type'], 'c')

    def test_get_3_days_forecast_fahrenheit(self):
        self.create_test_data(3)
        response = self.client.get(self.base_url, {'type': 'f'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 12)
        self.assertEqual(data['type'], 'f')

    def test_get_5_days_forecast_fahrenheit(self):
        self.create_test_data(5)
        response = self.client.get(self.base_url, {'days': 5, 'type': 'f'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 20)
        self.assertEqual(data['type'], 'f')

    def test_get_7_days_forecast_fahrenheit(self):
        self.create_test_data(7)
        response = self.client.get(self.base_url, {'days': 7, 'type': 'f'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 28)
        self.assertEqual(data['type'], 'f')

    def test_get_3_days_forecast_kelvin(self):
        self.create_test_data(3)
        response = self.client.get(self.base_url, {'type': 'k'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 12)
        self.assertEqual(data['type'], 'k')

    def test_get_5_days_forecast_kelvin(self):
        self.create_test_data(5)
        response = self.client.get(self.base_url, {'days': 5, 'type': 'k'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 20)
        self.assertEqual(data['type'], 'k')

    def test_get_7_days_forecast_kelvin(self):
        self.create_test_data(7)
        response = self.client.get(self.base_url, {'days': 7, 'type': 'k'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 28)
        self.assertEqual(data['type'], 'k')
