from datetime import datetime


from rest_framework import status
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response

from .serializers import ForecastSerializer
from .models import Forecast
from .schemas import ForecastsListFilterBackend, ForecastDateListFilterBackend


class ForecastList(generics.ListAPIView):
    serializer_class = ForecastSerializer
    filter_backends = (ForecastsListFilterBackend,)
    name = 'forecast-list'

    def get_queryset(self, *args, **kwargs):
        data = dict(
            temperature_type=self.request.query_params.get('type', 'c'),
            days=int(self.request.query_params.get('days', 3)),
            forecast_start_date=kwargs.get('forecast_start_date'),
        )
        queryset = Forecast.objects.forecasts_by_period(**data)
        return queryset

    def list(self, request, *args, **kwargs):
        forecast_start_date = kwargs.get('forecast_date', timezone.now().date())
        if isinstance(forecast_start_date, str):
            forecast_start_date = datetime.strptime(
                forecast_start_date, '%Y-%m-%d'
            ).date()

        if forecast_start_date < timezone.now().date():
            return Response(
                {'error': 'date must be greater or equal current date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset(forecast_start_date=forecast_start_date)
        serializer = self.get_serializer(queryset, many=True)
        result = {
            'type': request.query_params.get('type') or 'c',
            'forecasts': serializer.data
        }
        return Response(result)


class ForecastDateList(generics.ListAPIView):
    serializer_class = ForecastSerializer
    name = 'forecast-detail'
    lookup_field = 'forecast_date'
    filter_backends = (ForecastDateListFilterBackend,)

    def get_queryset(self, *args, **kwargs):
        data = dict(
            temperature_type=self.request.query_params.get('type', 'c'),
            request_hour=self.request.query_params.get('hour'),
        )
        queryset = Forecast.objects.forecasts_by_date(
            request_date=kwargs.get('request_date'),
            **data
        )
        return queryset

    def list(self, request, *args, **kwargs):
        request_date = kwargs.get('request_date', timezone.now().date())
        if isinstance(request_date, str):
            request_date = datetime.strptime(
                request_date, '%Y-%m-%d'
            ).date()
        if request_date > timezone.now().date():
            return Response(
                {'error': 'date must be less or equal current date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = self.get_queryset(request_date=request_date)
        serializer = self.get_serializer(queryset, many=True)
        result = {
            'type': request.query_params.get('type') or 'c',
            'temperature_data': serializer.data
        }
        return Response(result)
