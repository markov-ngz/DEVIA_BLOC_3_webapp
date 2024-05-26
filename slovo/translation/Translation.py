from django.views import View
from django.shortcuts import render
from dotenv import load_dotenv
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.functional import SimpleLazyObject
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
import logging
import os
import time
import sys
from datetime import datetime
from prom_exporter.views import COUNT_POSITIVE , COUNT_NEGATIVE, COUNT_REQ, COUNT_TRANSLATION , COUNT_FEEDBACK , TIME_TRANSLATION ,SIZE_BYTES_OUT, SIZE_BYTES_IN 
from .utils import get_client_browser , get_client_ip
from .translate import call_api_ai
from .forms import TranslateForm, FeedbackForm
from .models import Translation

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Translation(View):
    
    api_ai_url=os.getenv('API_AI_URL')
    login_url = api_ai_url+"/login"
    translate_url = api_ai_url + "/translation"
    feedback_url = api_ai_url + "/translation/feedback"

    def get(self,request:WSGIRequest)->HttpResponse:
        form = TranslateForm()
        return render(request,'translation/translation.html',{'form':form,'feedback':False})
    
    @csrf_protect
    def post(self,request:WSGIRequest)->HttpResponse:
        logger.info(f"{request.method} {request.get_full_path()} ; IP_CLIENT : {get_client_ip(request)} ; HTTP_SEC_CH_UA : { get_client_browser(request)}")
        user = request.user
        COUNT_REQ.inc()
        if 'translate' in request.POST :
            COUNT_TRANSLATION.inc()
            form = TranslateForm(request.POST)
            translation = self.translate(form,call_api_ai)
            if translation['translation'] == '':
                form = TranslateForm()
                return render(request,'translation/translation.html',{'form':form,'feedback':False,'error':True})
            second_form = FeedbackForm(translation)
            return render(request,'translation/translation.html',{'form':second_form,'feedback':True})
        elif 'feedback' in request.POST :
            COUNT_FEEDBACK.inc()
            form = FeedbackForm(request.POST)
            feedback = request.POST['feedback']
            self.send_feedback(form,feedback, user,call_api_ai,self.feedback_url,self.login_url)
            return render(request,'translation/translation.html',{'form':form,'feedback':False,'thanks':True})
        
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
                logger.info(f" Successfully sent feedback ")
            else:
                logger.error(f"Feedback could not be sent ")
        else:
            logger.info(f"Form data could not be validated for user {user.__str__()}")

    def translate(self,form:TranslateForm,api_func):
        """
        Validate the Translation form and call the API  to translate the text
        """
        if form.is_valid() :
            text = {'text': form.cleaned_data['text']}
            # metrics 
            size_payload = sys.getsizeof(text)
            SIZE_BYTES_IN.observe(size_payload)

            # make api call + metrics
            start = time.time()
            response = api_func(text,self.translate_url, self.login_url)
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
