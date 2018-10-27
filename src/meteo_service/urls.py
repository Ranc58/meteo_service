
from django.contrib import admin
from django.urls import path, re_path
from rest_framework_swagger.views import get_swagger_view

from meteo_api.views import ForecastList, TemperatureList


schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('a/v1/doc', schema_view),
    re_path('a/v1/temperature/forecasts/(?P<start_date>\d{4}-\d{2}-\d{2})', ForecastList.as_view()),
    re_path('a/v1/temperature/(?P<forecast_date>\d{4}-\d{2}-\d{2})', TemperatureList.as_view()),

]

