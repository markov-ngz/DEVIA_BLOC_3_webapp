from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from .forms import SignupForm, UpdateUserForm, PasswordForm, LoginForm
from .utils import get_client_browser, get_client_ip
import logging
from datetime import datetime
from django.contrib.auth.models import User 
from prom_exporter.views import COUNT_REQ, COUNT_HOME, COUNT_LOGOUT, COUNT_SIGNUP
from django.contrib.auth import authenticate, login

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@require_http_methods(["GET"])
def about(request):
    return render(request,"core/about.html")

@require_http_methods(["GET"])
def contact(request):
    return render(request,"core/contact.html")

@require_http_methods(["GET"])
def privacy(request):
    return render(request,"core/privacy.html")

@require_http_methods(["GET"])
def terms_of_use(request):
    return render(request,"core/terms_of_use.html")

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
            logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] New User saved")
            return redirect('/login/')
        else:
            logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] Invalid Form")
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
    logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] User succesfully logged out")
    return redirect('/')

def credentials_taken(username:str,email:str,user_pk:int)->bool:
    """
    Check if the credentials already exists in base 
    """
    if User.objects.exclude(pk=user_pk).filter(username=username).exists() or  User.objects.exclude(pk=user_pk).filter(email=email).exists() :

        return True 
    return False 
@login_required
def settings(request:WSGIRequest)->HttpResponse:
    user = request.user
    message = False
    if request.method == 'POST':
        if 'email_username' in request.POST:
            form = UpdateUserForm(request.POST)
            if form.is_valid():
                new_username = form.cleaned_data['username']
                new_email = form.cleaned_data["email"]
                if not credentials_taken(new_username,new_email,user.id) :
   
                    user.username = new_username
                    user.email = new_email
                    user.save()
                    return redirect('/logout')
                else : 
                    message = "Credentials are already taken "
        elif 'password' in request.POST : 
            form_pwd = PasswordForm(request.POST)
            if form_pwd.is_valid():
                data = form_pwd.cleaned_data
                if user.check_password(data['former_pwd']):
                    if data['confirm_pwd'] == data['new_pwd']:
                        user.set_password(data['new_pwd'])
                        user.save()
                        return redirect('/')
                    else : 
                        message = "new password and its confirmation do not match"
                        # display error message 'new password and its confirmation do not match'
                else : 
                    message = "Password could not be validated, if it is forgotten, please reset this one "
                    # Password could not be validated, if you forget , reset this one 
    form = UpdateUserForm({"username":user.username, "email":user.email})
    form_pwd = PasswordForm()
    return render(request,'core/settings.html',{'user':user,'form':form,'form_pwd':form_pwd,"message":message})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect("/")
    return render(request,'core/delete.html')

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            if user != None:
                user.last_login = datetime.now()
                user.save()
                login(request,user=user)
                return redirect("/")   

    return render(request,'core/login.html',{'form':LoginForm})