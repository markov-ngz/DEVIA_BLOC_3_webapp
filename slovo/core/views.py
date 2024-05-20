from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from .forms import SignupForm
from .utils import get_client_browser, get_client_ip
import logging
from datetime import datetime
from prom_exporter.views import COUNT_REQ, COUNT_HOME, COUNT_LOGOUT, COUNT_SIGNUP

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@require_http_methods(["GET"])
def home(request:WSGIRequest)->HttpResponse:
    COUNT_REQ.inc()
    COUNT_HOME.inc()
    logger.info(f"{request.method} {request.get_full_path()} ; IP_CLIENT : {get_client_ip(request)} ; HTTP_SEC_CH_UA : { get_client_browser(request)}")
    return render(request,"core/home.html")

@csrf_protect
def signup(request:WSGIRequest)->HttpResponse:
    COUNT_REQ.inc()
    COUNT_SIGNUP.inc()
    logger.info(f"{request.method} {request.get_full_path()} ; IP_CLIENT : {get_client_ip(request)} ; HTTP_SEC_CH_UA : { get_client_browser(request)}")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f"[{datetime.now().strftime("%H:%M:%S")}] New User saved")
            return redirect('/login/')
        else:
            logger.info(f"[{datetime.now().strftime("%H:%M:%S")}] Invalid Form")
    else:
        form = SignupForm()

    return render(request, 'core/signup.html',{
        'form':form 
    })

@csrf_protect
@login_required
def logout_view(request:WSGIRequest)->HttpResponse:
    COUNT_REQ.inc()
    COUNT_LOGOUT.inc()
    logger.info(f"{request.method} {request.get_full_path()} ; IP_CLIENT : {get_client_ip(request)} ; HTTP_SEC_CH_UA : { get_client_browser(request)}")
    logout(request)
    logger.info(f"[{datetime.now().strftime("%H:%M:%S")}] User succesfully logged out")
    return redirect('/')