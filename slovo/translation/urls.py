from django.urls import path
from . import views 

app_name = 'translation'

urlpatterns = [
    path("",views.translate, name="translate"),
    path("feedback", views.feedback, name="feedback"),
]