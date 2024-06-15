from django.urls import path
from . import views 
from translation.Translation import Translation
from django.contrib.auth.decorators import login_required
app_name = 'translation'

urlpatterns = [
    # path("",views.translate, name="translate"),
    path("",login_required(Translation.as_view(),login_url='/login'), name="translate")
]