
from django.contrib import admin
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from meteo_api.views import ForecastList, ForecastDateList


schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('a/v1/temperature/forecasts/<str:forecast_date>', ForecastList.as_view()),
    path('a/v1/temperature/<str:request_date>', ForecastDateList.as_view()),
    path('a/v1/doc', schema_view)
]

