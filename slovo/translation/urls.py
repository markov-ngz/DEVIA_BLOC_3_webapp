from django.urls import path
from . import views 

app_name = 'translation'

urlpatterns = [
    path("",views.translate, name="translate"),
    path("fixtures",views.fixture, name="fixture")
]