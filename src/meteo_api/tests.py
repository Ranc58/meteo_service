import json
from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ForecastFactory


def create_test_data(days, yesterday=None):
    if yesterday:
        yesterday = timezone.now().replace(hour=0) - timedelta(days=1)
        for forecast_hour in range(0, 24):
            ForecastFactory(
                forecast_datetime=yesterday.replace(hour=forecast_hour)
            )
        return
    for forecast_day in range(days):
        day = timezone.now().replace(hour=0) + timedelta(days=forecast_day)
        for forecast_hour in range(0, 24):
            ForecastFactory(
                forecast_datetime=day.replace(hour=forecast_hour)
            )


class TestForecastsHandler(APITestCase):

    def setUp(self):
        self.base_url = '/a/v1/forecast'

    def test_get_3_days_forecast_celsius(self):
        create_test_data(3)
        response = self.client.get(self.base_url)
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 3*24)
        self.assertEqual(data['type'], 'c')

    def test_get_5_days_forecast_celsius(self):
        create_test_data(5)
        response = self.client.get(self.base_url, {'days': 5})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 5*24)
        self.assertEqual(data['type'], 'c')

    def test_get_7_days_forecast_celsius(self):
        create_test_data(7)
        response = self.client.get(self.base_url, {'days': 7})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 7*24)
        self.assertEqual(data['type'], 'c')

    def test_get_3_days_forecast_fahrenheit(self):
        create_test_data(3)
        response = self.client.get(self.base_url, {'type': 'f'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 3*24)
        self.assertEqual(data['type'], 'f')

    def test_get_5_days_forecast_fahrenheit(self):
        create_test_data(5)
        response = self.client.get(self.base_url, {'days': 5, 'type': 'f'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 5*24)
        self.assertEqual(data['type'], 'f')

    def test_get_7_days_forecast_fahrenheit(self):
        create_test_data(7)
        response = self.client.get(self.base_url, {'days': 7, 'type': 'f'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 7*24)
        self.assertEqual(data['type'], 'f')

    def test_get_3_days_forecast_kelvin(self):
        create_test_data(3)
        response = self.client.get(self.base_url, {'type': 'k'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 3*24)
        self.assertEqual(data['type'], 'k')

    def test_get_5_days_forecast_kelvin(self):
        create_test_data(5)
        response = self.client.get(self.base_url, {'days': 5, 'type': 'k'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 5*24)
        self.assertEqual(data['type'], 'k')

    def test_get_7_days_forecast_kelvin(self):
        create_test_data(7)
        response = self.client.get(self.base_url, {'days': 7, 'type': 'k'})
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 7*24)
        self.assertEqual(data['type'], 'k')


class TestForecastHandler(APITestCase):

    def setUp(self):
        self.base_url = '/a/v1/forecast/{}'

    def test_get_by_date_celsius(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date()))
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['day_forecasts']), 24)
        self.assertEqual(data['type'], 'c')

    def test_get_by_date_kelvin(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'type': 'k'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['day_forecasts']), 24)
        self.assertEqual(data['type'], 'k')

    def test_get_by_date_fahrenheit(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'type': 'f'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['day_forecasts']), 24)
        self.assertEqual(data['type'], 'f')

    def test_get_by_current_datetime_celsius(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'hour': 12}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['day_forecasts']), 1)
        self.assertEqual(data['type'], 'c')

    def test_get_by_current_datetime_fahrenheit(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'type': 'f', 'hour': 12}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['day_forecasts']), 1)
        self.assertEqual(data['type'], 'f')

    def test_get_by_current_datetime_kelvin(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'type': 'k', 'hour': 12}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['day_forecasts']), 1)
        self.assertEqual(data['type'], 'k')
