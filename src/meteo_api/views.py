from datetime import datetime, timedelta

from django.conf import settings
from rest_framework import status
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .serializers import TemperatureSerializer
from .models import Forecast
from .filters import PeriodFilter, TemperatureFilter


class TemperatureList(generics.ListAPIView):
    queryset = Forecast.objects.all()
    serializer_class = TemperatureSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = TemperatureFilter

    def get_queryset(self, *args, **kwargs):
        queryset = Forecast.objects.filter(
            forecast_datetime__contains=self.kwargs.get('request_date')
        )
        return queryset

    def list(self, request, *args, **kwargs):
        request_date = datetime.strptime(
            kwargs.get('forecast_date'), '%Y-%m-%d'
        ).date()
        if request_date > timezone.now().date():
            return Response(
                {'error': 'date must be less or equal current date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.kwargs.update({'request_date': request_date})
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        temperature_type = self.request.query_params.get('type', 'c')
        data = {
                   'temperature_type': temperature_type,
                   'meteo_data': serializer.data,
               }
        return Response(
            data,
            status=status.HTTP_200_OK
        )


class ForecastList(generics.ListAPIView):
    queryset = Forecast.objects.all()
    serializer_class = TemperatureSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = PeriodFilter

    def get_queryset(self, *args, **kwargs):
        forecast_start_date = self.kwargs.get('forecast_start_date')
        queryset = Forecast.objects.filter(
                forecast_datetime__gte=forecast_start_date
            )
        if self.request.query_params.get('days'):
            return queryset
        current_datetime = timezone.now().replace(hour=0, minute=0, second=0)
        max_date = current_datetime + timedelta(days=settings.DEFAULT_DAYS_PERIOD)
        queryset = queryset.filter(
            forecast_datetime__lte=max_date.replace(hour=23, minute=59, second=59)
        )
        return queryset

    def list(self, request, *args, **kwargs):
        forecast_start_date = datetime.strptime(
            kwargs.get('start_date'), '%Y-%m-%d'
        ).date()
        if forecast_start_date < timezone.now().date():
            return Response(
                {'error': 'date must be greater or equal current date'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.kwargs.update({'forecast_start_date': forecast_start_date})
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        temperature_type = self.request.query_params.get('type', 'c')
        data = {
                   'temperature_type': temperature_type,
                   'meteo_data': serializer.data,
               }
        return Response(
            data,
            status=status.HTTP_200_OK
        )
