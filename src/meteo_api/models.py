from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Forecast(models.Model):
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
        result = self.temperature + 273.15
        return round(result, 2)

