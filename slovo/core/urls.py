from django.contrib.auth import views as auth_views
from django.urls import path
from . import views 
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path("",views.home, name="home"),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout_view, name='logout'),
    path('login/',views.login_user, name='login'),
    path('settings/',views.settings,name="settings"),
    path('delete/',views.delete_account,name="delete"),
    path('terms_of_use/',views.terms_of_use, name="terms_of_use"),
    path('about/',views.about, name="about"),
    path('privacy/',views.privacy, name="privacy"),
    path('contact/',views.contact, name="contact"),
]