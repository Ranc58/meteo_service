from datetime import datetime, timedelta

from django_filters.rest_framework import FilterSet
from django_filters import rest_framework as filters

from .models import Forecast


class TemperatureFilter(FilterSet):
    hour = filters.CharFilter(method='filter_hour', label='Current hour')

    def filter_hour(self, queryset, name, value):
        if value:
            return queryset.filter(forecast_datetime__hour=value)
        return queryset

    class Meta:
        model = Forecast
        exclude = ['temperature', 'forecast_datetime', 'created_dttm']


class PeriodFilter(FilterSet):
    days = filters.CharFilter(method='filter_period', label='By days')
    hour = filters.CharFilter(method='filter_hour', label='Current hour')

    def filter_period(self, queryset, name, value):
        start_date_str = self.request.parser_context['kwargs']['start_date']
        forecast_start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        days_count = int(value) or 3
        if days_count > 7:
            days_count = 7
        elif days_count <= 0:
            days_count = 3
        max_date = forecast_start_date + timedelta(days=days_count)
        queryset = Forecast.objects.filter(
            forecast_datetime__gte=forecast_start_date,
            forecast_datetime__lt=max_date
        )
        return queryset

    def filter_hour(self, queryset, name, value):
        if value:
            return queryset.filter(forecast_datetime__hour=value)
        return queryset

    class Meta:
        model = Forecast
        exclude = ['temperature', 'forecast_datetime', 'created_dttm']
