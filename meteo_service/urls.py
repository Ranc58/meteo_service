
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from meteo_api.views import ForecastList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('a/v1/forecast', ForecastList.as_view())
]

