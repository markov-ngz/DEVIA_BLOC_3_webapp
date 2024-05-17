from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import requests , json , os
from requests import RequestException
import logging
from datetime import datetime
from .forms import TranslateForm
from .translate import make_translation




logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


    
# Create your views here.
@csrf_protect
# @login_required(login_url='/login')
@require_http_methods(["POST","GET"])
def translate(request):
    if request.method == 'POST':
        form = TranslateForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data
            translation = make_translation(text)

            if translation['translation'].endswith('.'): # weird model interaction
                translation['translation'] = translation['translation'][:-1]
        else:
            translation = ""
        return render(request,'translation/translation.html',{'form':form,"translation":translation['translation']})
    else:
        translation= ""
        form = TranslateForm()
        return render(request,'translation/translation.html',{'form':form,"translation":translation})