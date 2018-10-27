from datetime import datetime

from django.conf import settings
from rest_framework import serializers

from .models import Forecast


class TemperatureSerializer(serializers.ModelSerializer):
    temperature = serializers.SerializerMethodField()
    datetime = serializers.SerializerMethodField()

    def get_temperature(self, obj):
        request = self.context.get('request')
        temperature_type = request.query_params.get('type')
        temperature = obj.temperature
        if temperature_type == 'f':
            temperature = obj.get_in_fahrenheit
        elif temperature_type == 'k':
            temperature = obj.get_in_kelvin
        return temperature

    def get_datetime(self, obj):
        forecast_datetime = datetime.strftime(
            obj.forecast_datetime,
            settings.DATETIME_FORMAT
        )
        return forecast_datetime

    class Meta:
        model = Forecast
        fields = [
            'datetime',
            'temperature',
        ]
