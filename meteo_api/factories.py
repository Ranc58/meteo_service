import random


import factory
from django.utils import timezone


class ForecastFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'meteo_api.Forecast'

    temperature = random.randint(-30, 30)
    forecast_datetime = timezone.now()
