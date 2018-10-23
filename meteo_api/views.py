from datetime import datetime, timedelta

from django.db.models import F
from django.conf import settings
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import ForecastSerializer
from .models import Forecast


class ForecastList(generics.ListAPIView):
    serializer_class = ForecastSerializer
    name = 'forecast-list'

    def get_queryset(self):
        data = dict(
            temperature_type=self.request.query_params.get('type', 'c'),
            days=int(self.request.query_params.get('days', 3))
        )
        queryset = Forecast.objects.forecasts_by_period(**data)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        result = {
            'type': self.request.query_params.get('type') or 'c',
            'forecasts': serializer.data
        }
        return Response(result)


class ForecastDateList(generics.ListAPIView):
    serializer_class = ForecastSerializer
    name = 'forecast-detail'
    lookup_field = 'forecast_date'

    def get_queryset(self, *args, **kwargs):
        data = dict(
            temperature_type=self.request.query_params.get('type', 'c'),
            forecast_hour=self.request.query_params.get('hour'),
        )
        queryset = Forecast.objects.forecasts_by_date(forecast_date=kwargs.get('forecast_date'), **data)
        return queryset

    def list(self, request, *args, **kwargs):
        forecast_date = kwargs.get('forecast_date')
        queryset = self.get_queryset(forecast_date=forecast_date)
        serializer = self.get_serializer(queryset, many=True)
        result = {
            'type': self.request.query_params.get('type') or 'c',
            'day_forecasts': serializer.data
        }
        return Response(result)

