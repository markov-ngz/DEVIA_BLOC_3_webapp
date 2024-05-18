from django.shortcuts import render, get_object_or_404, redirect
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
from .translate import make_translation

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def validate_and_call(form:TranslateForm,api_func)->dict:
    """
    Validate the form and call the API with the function provided
    """
    if form.is_valid() :
        text = {'text': form.cleaned_data['text']}
        # translation = api_func(text)
        translation = {"text":form.cleaned_data['text'],"translation":"Dzien dobry"}
        if isinstance(translation,dict):
            if translation['translation'].endswith('.'): # weird model interaction
                translation['translation'] = translation['translation'][:-1]
        else:
            translation = {"translation":""}
    else:
        translation = {"translation":""} 
    
    return translation

def save_feedback(form:FeedbackForm,feedback:str, user:SimpleLazyObject)->None:
    """
    Save the feedback form into database
    """
    if form.is_valid() :
        is_correct = True if feedback == 'Pozytywny' else False
        print(is_correct)
        form_data = form.cleaned_data 
        translation = Translation(text=form_data['text'],translation=form_data['translation'], is_correct=is_correct)
        translation.created_by = user
        try:
            translation.save()
        except Exception as e :
            logger.error(f"[{datetime.now()}] Error: could not save form data {str(e)}")
    else:
        logger.info(f"[{datetime.now()}] Form data could not be validated for user {user.__str__()}")


@csrf_protect
@login_required(login_url='/login')
@require_http_methods(["POST","GET"])
def translate(request:WSGIRequest)->HttpResponse:
    user = request.user
    if request.method == 'POST' and ('translate' in request.POST or 'feedback' in request.POST):
        if 'translate' in request.POST :
            form = TranslateForm(request.POST)
            translation = validate_and_call(form,make_translation)
            second_form = FeedbackForm(translation)
            return render(request,'translation/translation.html',{'form':second_form,'feedback':True})
        elif 'feedback' in request.POST :
            form = FeedbackForm(request.POST)
            feedback = request.POST['feedback']
            print(feedback)
            save_feedback(form,feedback, user)
            return render(request,'translation/translation.html',{'form':form,'feedback':False,'thanks':True})
    else:
        form = TranslateForm()
        return render(request,'translation/translation.html',{'form':form,'feedback':False})
    