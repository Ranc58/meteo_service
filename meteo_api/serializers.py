from rest_framework import serializers


class ForecastSerializer(serializers.Serializer):
    forecast_temperature = serializers.FloatField()
    forecast_datetime = serializers.DateTimeField()
