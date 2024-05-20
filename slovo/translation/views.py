import logging
import os
import time
import sys
from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.functional import SimpleLazyObject
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse
from dotenv import load_dotenv
from .models import Translation
from .forms import TranslateForm, FeedbackForm
from .translate import call_api_ai
from .utils import get_client_browser , get_client_ip
from prom_exporter.views import COUNT_POSITIVE , COUNT_NEGATIVE, COUNT_REQ, COUNT_TRANSLATION , COUNT_FEEDBACK , TIME_TRANSLATION ,SIZE_BYTES_OUT, SIZE_BYTES_IN 

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


API_AI_URL=os.getenv('API_AI_URL')
LOGIN_URL = API_AI_URL+"/login"
TRANSLATE_URL = API_AI_URL + "/translation"
FEEDBACK_URL = API_AI_URL + "/translation/feedback"

def validate_and_call(form:TranslateForm,api_func):
    """
    Validate the Translation form and call the API  to translate the text
    """
    TIME_TRANSLATION ,SIZE_BYTES_OUT, SIZE_BYTES_IN 
    if form.is_valid() :
        text = {'text': form.cleaned_data['text']}
        # metrics 
        size_payload = sys.getsizeof(text)
        SIZE_BYTES_IN.observe(size_payload)

        # make api call + metrics
        start = time.time()
        response = api_func(text,TRANSLATE_URL, LOGIN_URL)
        TIME_TRANSLATION.observe(time.time()- start )

        # instiate the dict for the response
        translation = {"text":form.cleaned_data['text']}

        if isinstance(response,dict):
            SIZE_BYTES_OUT.observe(sys.getsizeof(response))
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
        COUNT_POSITIVE.inc() if is_correct else COUNT_NEGATIVE.inc()
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
    COUNT_REQ.inc()
    if request.method == 'POST' and ('translate' in request.POST or 'feedback' in request.POST):
        if 'translate' in request.POST :
            COUNT_TRANSLATION.inc()
            form = TranslateForm(request.POST)
            translation = validate_and_call(form,call_api_ai)
            if translation['translation'] == '':
                form = TranslateForm()
                return render(request,'translation/translation.html',{'form':form,'feedback':False,'error':True})
            second_form = FeedbackForm(translation)
            return render(request,'translation/translation.html',{'form':second_form,'feedback':True})
        elif 'feedback' in request.POST :
            COUNT_FEEDBACK.inc()
            form = FeedbackForm(request.POST)
            feedback = request.POST['feedback']
            send_feedback(form,feedback, user,call_api_ai,FEEDBACK_URL,LOGIN_URL)
            return render(request,'translation/translation.html',{'form':form,'feedback':False,'thanks':True})
    else:
        form = TranslateForm()
        return render(request,'translation/translation.html',{'form':form,'feedback':False})
    