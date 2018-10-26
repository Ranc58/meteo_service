from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class ForecastQuerySet(models.QuerySet):

    def _build_meteo_list(self, forecasts, temperature_type):
        values = []
        if temperature_type == 'f':
            for x in forecasts:
                x.forecast_temperature = x.get_in_fahrenheit
                values.append(x)
        elif temperature_type == 'k':
            for x in forecasts:
                x.forecast_temperature = x.get_in_kelvin
                values.append(x)
        else:
            for x in forecasts:
                x.forecast_temperature = x.temperature
                values.append(x)
        return values

    def forecasts_by_period(self, temperature_type, days, forecast_start_date):
        if days > 7:
            days = 7
        elif days <= 0:
            days = 3
        max_date = forecast_start_date + timedelta(days=days)
        queryset = Forecast.objects.filter(
            forecast_datetime__gte=forecast_start_date,
            forecast_datetime__lte=max_date
        )
        forecasts = self._build_meteo_list(queryset, temperature_type)
        return forecasts

    def forecasts_by_date(self, request_date, temperature_type, request_hour=None):
        queryset = Forecast.objects.filter(forecast_datetime__contains=request_date)
        if request_hour:
            queryset = queryset.filter(forecast_datetime__hour=request_hour)
        forecasts = self._build_meteo_list(queryset, temperature_type)
        return forecasts


class Forecast(models.Model):
    objects = ForecastQuerySet.as_manager()
    temperature = models.FloatField(verbose_name=_('Temperature'))
    forecast_datetime = models.DateTimeField(verbose_name=_('Forecast datetime'))
    created_dttm = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.forecast_datetime}"

    @property
    def get_in_fahrenheit(self):
        result = (self.temperature * 9/5) + 32
        return round(result, 2)

    @property
    def get_in_kelvin(self):
        result = self.temperature * + 273.15
        return round(result, 2)

