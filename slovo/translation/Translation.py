from django.views import View
from django.shortcuts import render , redirect
from dotenv import load_dotenv
from django.http.response import HttpResponse
from django.utils.functional import SimpleLazyObject
from django.core.handlers.wsgi import WSGIRequest
import logging
import os
import time
import sys
from prom_exporter.views import COUNT_POSITIVE , COUNT_NEGATIVE, COUNT_REQ, COUNT_TRANSLATION , COUNT_FEEDBACK , TIME_TRANSLATION ,SIZE_BYTES_OUT, SIZE_BYTES_IN 
from .utils import get_client_browser , get_client_ip
from .forms import TranslateForm, FeedbackForm
from .models import Translation_stats
from translation.ApiHandler import ApiHandler
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Translation(View):
    
    api_ai_url=os.getenv('API_AI_URL')
    login_url = api_ai_url+"/login"
    translate_url = api_ai_url + "/translation"
    feedback_url = api_ai_url + "/translation/feedback"
    pos_feedback = 'Pozytywny'
    api_handler = ApiHandler(os.getenv('API_AI_URL'))
    
    def get(self,request:WSGIRequest)->HttpResponse:
        form = TranslateForm()
        return render(request,'translation/translation.html',{'form':form,'feedback':False})
    

    def post(self,request:WSGIRequest)->HttpResponse:
        logger.info(f"{request.method} {request.get_full_path()} ; IP_CLIENT : {get_client_ip(request)} ; HTTP_SEC_CH_UA : { get_client_browser(request)}")
        user = request.user
        user_stats = Translation_stats.objects.get_or_create(user_id=user)[0]
        COUNT_REQ.inc()
        if 'translate' in request.POST :
            COUNT_TRANSLATION.inc()
            form = TranslateForm(request.POST)
            if form.is_valid():
                translation = self.translate(form)
                if translation['translation'] == '':
                    form = TranslateForm()
                    return render(request,'translation/translation.html',{'form':form,'feedback':False,'error':True})
                second_form = FeedbackForm(translation)
                user_stats.count_translations += 1
                user_stats.save()
                return render(request,'translation/translation.html',{'form':second_form,'feedback':True})
        elif 'feedback' in request.POST :
            COUNT_FEEDBACK.inc()
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feedback = request.POST['feedback']
                user_stats.count_feedbacks += 1
                self.send_feedback(form,feedback, user)
                if feedback == self.pos_feedback:
                    user_stats.count_pos_feedbacks +=1
                else:
                    user_stats.count_neg_feedbacks +=1 
                user_stats.save()
                return render(request,'translation/translation.html',{'form':form,'feedback':False,'thanks':True})
            
        return redirect("/translate")
        
    def send_feedback(self,form:FeedbackForm,feedback:str, user:SimpleLazyObject)->None:
        """
        Save the feedback form into database
        """

        if form.is_valid() :
            is_correct = True if feedback == 'Pozytywny' else False
            COUNT_POSITIVE.inc() if is_correct else COUNT_NEGATIVE.inc()
            form_data = form.cleaned_data 
            form_data['is_correct'] = is_correct
            response = self.api_handler.call_api_ai(form_data,self.feedback_url)
            if response:
                logger.info(f" Successfully sent feedback ")
            else:
                logger.error(f"Feedback could not be sent ")
        else:
            logger.info(f"Form data could not be validated for user {user.__str__()}")

    def translate(self,form:TranslateForm):
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
            response = self.api_handler.call_api_ai(text,self.translate_url)
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
