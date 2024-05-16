from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import requests , json 
from .forms import TranslateForm

def request_translation(payload):
    # get bearer 
    headers = {}
    try:
        req = requests.post("",json=payload)
        return req.json()
    except:
        return  None
# Create your views here.
@csrf_protect
# @login_required(login_url='/login')
@require_http_methods(["POST","GET"])
def translate(request):
    if request.method == 'POST':
        form = TranslateForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data
            translation = "Dzien dobry"
            form_bis = TranslateForm()
            # make request , handle errors 
        else:
            translation = ""
        return render(request,'translation/translation.html',{'form':form,"translation":translation})
    else:
        translation= ""
        form = TranslateForm()
        return render(request,'translation/translation.html',{'form':form,"translation":translation})