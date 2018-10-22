from django.db import models
from django.utils.translation import ugettext_lazy as _


class Forecast(models.Model):

    temperature_celsius = models.FloatField(verbose_name=_('Temperature'))
    forecast_datetime = models.DateTimeField(verbose_name=_('Forecast datetime'))
    created_dttm = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.forecast_datetime}"

