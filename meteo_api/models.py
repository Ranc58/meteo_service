from datetime import datetime, timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _


class ForecastQuerySet(models.QuerySet):

    def forecasts_period(self, temperature_type, days):
        current_day = datetime.now()
        max_date = current_day + timedelta(days=days)
        queryset = Forecast.objects.filter(
            forecast_datetime__gte=current_day.date(),
            forecast_datetime__lte=max_date.date()
        )
        values = []
        if temperature_type and temperature_type == 'f':
            for x in queryset:
                x.forecast_temperature = x.get_in_fahrenheit
                values.append(x)
        elif temperature_type and temperature_type == 'k':
            for x in queryset:
                x.forecast_temperature = x.get_in_kelvin
                values.append(x)
        else:
            for x in queryset:
                x.forecast_temperature = x.temperature
                values.append(x)
        return values or queryset


class Forecast(models.Model):
    objects = ForecastQuerySet.as_manager()
    temperature = models.FloatField(verbose_name=_('Temperature'))
    forecast_datetime = models.DateTimeField(verbose_name=_('Forecast datetime'))
    created_dttm = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.forecast_datetime}"

    @property
    def get_in_fahrenheit(self):
        return (self.temperature * 9/5) + 32

    @property
    def get_in_kelvin(self):
        return self.temperature * + 273.15

