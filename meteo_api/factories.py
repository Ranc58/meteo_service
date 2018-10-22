import random
from datetime import datetime

import factory
from django.utils import timezone


class ForecastFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'meteo_api.Forecast'

    temperature = random.randint(-10, 30)
    forecast_datetime = datetime.now(tz=timezone.utc)
