import json

from rest_framework.test import APITestCase
from rest_framework import status

from .factories import ForecastFactory


class TestForecastsHandler(APITestCase):

    def setUp(self):
        self.base_url = '/a/v1/forecast'

    def test_get_3_days_forecast_celsius(self):
        for _ in range(3):
            ForecastFactory()
        response = self.client.post(self.base_url)
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 3)

    def test_get_5_days_forecast_celsius(self):
        for _ in range(5):
            ForecastFactory()
        response = self.client.post(self.base_url)
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 5)

    def test_get_7_days_forecast_celsius(self):
        for _ in range(7):
            ForecastFactory()
        response = self.client.post(self.base_url)
        data = json.loads(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data['forecasts']), 7)

