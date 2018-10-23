from datetime import datetime, timedelta
import random

from django.core.management.base import BaseCommand
from meteo_api import factories


class Command(BaseCommand):
    help = 'Create forecasts from 1 november 2016.'

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def handle(self, *args, **options):
        start_date = datetime.strptime('Nov 1 2016', '%b %d %Y')
        end_date = datetime.now()
        for single_date in self.daterange(start_date, end_date):
            for forecast_hour in range(0, 24):
                factories.ForecastFactory(
                    forecast_datetime=single_date.replace(hour=forecast_hour),
                    temperature=random.randint(-30, 30)
                )