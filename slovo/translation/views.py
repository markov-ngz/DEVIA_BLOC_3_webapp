from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import requests , json 
# Create your views here.
@csrf_protect
# @login_required(login_url='/login')
@require_http_methods(["POST","GET"])
def translate(request):
    return render(request,'translation/translation.html')