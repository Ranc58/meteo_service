import random
from datetime import datetime

import factory


class ForecastFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'meteo_api.Forecast'

    temperature_celsius = random.randint()
    forecast_datetime = datetime.now()
