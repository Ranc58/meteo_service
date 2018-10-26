from datetime import datetime, timedelta
import random

import pytz
from django.core.management.base import BaseCommand
from django.utils import timezone
from meteo_api import factories


class Command(BaseCommand):
    help = 'Create forecasts from 1 november 2016.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--week',
            action='store_true',
            dest='week',
            help='Create forecasts for the week ahead',
        )

    def daterange(self, start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def handle(self, *args, **options):
        start_date = datetime.strptime('2016-11-01', '%Y-%m-%d')
        start_date = start_date.replace(tzinfo=pytz.UTC)
        end_date = timezone.now()
        if options['week']:
            end_date = end_date + timedelta(days=7)
        for single_date in self.daterange(start_date, end_date):
            for forecast_hour in range(0, 24):
                factories.ForecastFactory(
                    forecast_datetime=single_date.replace(hour=forecast_hour),
                    temperature=random.randint(-30, 30)
                )
