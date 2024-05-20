from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.functional import SimpleLazyObject
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
import logging
from datetime import datetime
from .models import Translation
from .forms import TranslateForm, FeedbackForm
from .translate import call_api_ai
import os
from dotenv import load_dotenv
from .utils import get_client_browser , get_client_ip
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


API_AI_URL=os.getenv('API_AI_URL')
LOGIN_URL = API_AI_URL+"/login"
TRANSLATE_URL = API_AI_URL + "/translation"
FEEDBACK_URL = API_AI_URL + "/translation/feedback"

def validate_and_call(form:TranslateForm,api_func):
    """
    Validate the form and call the API with the function provided
    """
    if form.is_valid() :
        text = {'text': form.cleaned_data['text']}
        response = api_func(text,TRANSLATE_URL, LOGIN_URL)
        translation = {"text":form.cleaned_data['text']}
        if isinstance(response,dict):
            if response['translation'].endswith('.'): # weird model interaction
                translation['translation'] = response['translation'][:-1]
            else:
                translation['translation'] = response['translation']
        else:
            translation['translation']  = ""
    else:
        translation = False
    
    return translation

def save_feedback(payload:dict, user:SimpleLazyObject)->None:
    """
    Save the feedback form into database along with its user
    """
    translation = Translation(text=payload['text'],translation=payload['translation'],is_correct=payload['is_correct'])
    translation.created_by = user
    try:
        translation.save()
    except Exception as e :
        logger.error(f"[{datetime.now()}] Error: could not save form data {str(e)}")

def send_feedback(form:FeedbackForm,feedback:str, user:SimpleLazyObject,api_func,feedback_url:str,login_url:str)->None:
    """
    Save the feedback form into database
    """
    if form.is_valid() :
        is_correct = True if feedback == 'Pozytywny' else False
        form_data = form.cleaned_data 
        form_data['is_correct'] = is_correct
        response = api_func(form_data,feedback_url,login_url,201)
        if response:
            logger.info(f"[{datetime.now().strftime("%H:%M:%S")}] Successfully sent feedback ")
        else:
            logger.error(f"[{datetime.now().strftime("%H:%M:%S")}] Feedback could not be sent ")
    else:
        logger.info(f"[{datetime.now().strftime("%H:%M:%S")}] Form data could not be validated for user {user.__str__()}")


@csrf_protect
@login_required(login_url='/login')
@require_http_methods(["POST","GET"])
def translate(request:WSGIRequest)->HttpResponse:
    logger.info(f"{request.method} {request.get_full_path()} ; IP_CLIENT : {get_client_ip(request)} ; HTTP_SEC_CH_UA : { get_client_browser(request)}")
    user = request.user
    if request.method == 'POST' and ('translate' in request.POST or 'feedback' in request.POST):
        if 'translate' in request.POST :
            form = TranslateForm(request.POST)
            translation = validate_and_call(form,call_api_ai)
            second_form = FeedbackForm(translation)
            return render(request,'translation/translation.html',{'form':second_form,'feedback':True})
        elif 'feedback' in request.POST :
            form = FeedbackForm(request.POST)
            feedback = request.POST['feedback']
            send_feedback(form,feedback, user,call_api_ai,FEEDBACK_URL,LOGIN_URL)
            return render(request,'translation/translation.html',{'form':form,'feedback':False,'thanks':True})
    else:
        form = TranslateForm()
        return render(request,'translation/translation.html',{'form':form,'feedback':False})
    