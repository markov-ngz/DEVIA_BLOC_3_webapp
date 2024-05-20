from django.urls import path
from . import views 

app_name = 'prom_exporter'

urlpatterns = [
    path("metrics",views.metrics, name="metrics"),
]