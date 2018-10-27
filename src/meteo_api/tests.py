import json
from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ForecastFactory


def create_test_data(days, yesterday=None):
    for forecast_day in range(days):
        day = timezone.now().replace(hour=0, minute=0, second=0) + timedelta(days=forecast_day)
        if yesterday:
            day = timezone.now().replace(hour=0, minute=0, second=0) - timedelta(days=forecast_day)
        for forecast_hour in range(0, 24):
            ForecastFactory(
                forecast_datetime=day.replace(hour=forecast_hour)
            )


class TestForecastsHandler(APITestCase):

    def setUp(self):
        self.base_url = '/a/v1/temperature/forecasts/{}'

    def test_get_yesterday_forecast(self):
        create_test_data(5)
        yesterday_date = timezone.now().date() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(yesterday_date)
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data['error'], 'date must be greater or equal current date')

    def test_get_3_days_forecast_celsius_current_time(self):
        create_test_data(10)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'hour': 5}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 3)
        self.assertEqual(data['temperature_type'], 'c')

    def test_get_3_days_forecast_celsius(self):
        create_test_data(10)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date)
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 3*24)
        self.assertEqual(data['temperature_type'], 'c')

    def test_get_5_days_forecast_celsius(self):
        create_test_data(10)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'days': 5}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 5*24)
        self.assertEqual(data['temperature_type'], 'c')

    def test_get_7_days_forecast_celsius(self):
        create_test_data(10)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'days': 7}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 7*24)
        self.assertEqual(data['temperature_type'], 'c')

    def test_get_3_days_forecast_fahrenheit(self):
        create_test_data(10)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'type': 'f'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 3*24)
        self.assertEqual(data['temperature_type'], 'f')

    def test_get_5_days_forecast_fahrenheit(self):
        create_test_data(8)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'days': 5, 'type': 'f'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 5*24)
        self.assertEqual(data['temperature_type'], 'f')

    def test_get_7_days_forecast_fahrenheit(self):
        create_test_data(10)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'days': 7, 'type': 'f'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 7*24)
        self.assertEqual(data['temperature_type'], 'f')

    def test_get_3_days_forecast_kelvin(self):
        create_test_data(8)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'type': 'k'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 3*24)
        self.assertEqual(data['temperature_type'], 'k')

    def test_get_5_days_forecast_kelvin(self):
        create_test_data(8)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'days': 5, 'type': 'k'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 5*24)
        self.assertEqual(data['temperature_type'], 'k')

    def test_get_7_days_forecast_kelvin(self):
        create_test_data(10)
        tomorrow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tomorrow_date),
            {'days': 7, 'type': 'k'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 7*24)
        self.assertEqual(data['temperature_type'], 'k')


class TestForecastHandler(APITestCase):

    def setUp(self):
        self.base_url = '/a/v1/temperature/{}'

    def test_get_tommorow_temperature(self):
        create_test_data(5)
        tommorow_date = timezone.now().date() + timedelta(days=1)
        response = self.client.get(
            self.base_url.format(tommorow_date)
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data['error'], 'date must be less or equal current date')

    def test_get_by_date_celsius(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date()))
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 24)
        self.assertEqual(data['temperature_type'], 'c')

    def test_get_by_date_kelvin(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'type': 'k'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 24)
        self.assertEqual(data['temperature_type'], 'k')

    def test_get_by_date_fahrenheit(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'type': 'f'}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 24)
        self.assertEqual(data['temperature_type'], 'f')

    def test_get_by_current_datetime_celsius(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'hour': 12}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 1)
        self.assertEqual(data['temperature_type'], 'c')

    def test_get_by_current_datetime_fahrenheit(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'type': 'f', 'hour': 12}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 1)
        self.assertEqual(data['temperature_type'], 'f')

    def test_get_by_current_datetime_kelvin(self):
        create_test_data(3, yesterday=True)
        yesterday = timezone.now() - timedelta(days=1)
        response = self.client.get(
            self.base_url.format(str(yesterday.date())),
            {'type': 'k', 'hour': 12}
        )
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['meteo_data']), 1)
        self.assertEqual(data['temperature_type'], 'k')
