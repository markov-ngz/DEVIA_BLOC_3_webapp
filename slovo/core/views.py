from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from .forms import SignupForm

@require_http_methods(["GET"])
def home(request:WSGIRequest)->HttpResponse:
    return render(request,"core/home.html")

@csrf_protect
def signup(request:WSGIRequest)->HttpResponse:
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html',{
        'form':form 
    })

@csrf_protect
@login_required
def logout_view(request:WSGIRequest)->HttpResponse:
    logout(request)
    return redirect('/')