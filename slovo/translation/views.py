from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import logging
from datetime import datetime
from .models import Translation
from .forms import TranslateForm, FeedbackForm
from .translate import make_translation

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@csrf_protect
# @login_required(login_url='/login')
@require_http_methods(["POST","GET"])
def translate(request):
    print(request.user)
    if request.method == 'POST' and ('translate' in request.POST or 'feedback' in request.POST):
        if 'translate' in request.POST :
            form = TranslateForm(request.POST)
            if form.is_valid() :
                text = {'text': form.cleaned_data['text']}
                # translation = make_translation(text)
                translation = {"text":form.cleaned_data['text'],"translation":"Dzien dobry"}
                if isinstance(translation,dict):
                    if translation['translation'].endswith('.'): # weird model interaction
                        translation['translation'] = translation['translation'][:-1]
                else:
                    translation = {"translation":""}
            else:
                translation = {"translation":""}
            second_form = FeedbackForm(translation)
            return render(request,'translation/translation.html',{'form':second_form,"translation":translation['translation']})
        elif 'feedback' in request.POST :
            form = FeedbackForm(request.POST)
            if form.is_valid() :
                form_data = form.cleaned_data 
                translation = Translation(text=form_data['text'],translation=form_data['translation'])
                translation.save()
            return render(request,'translation/translation.html',{'form':form})
    else:
        translation= {"translation":""}
        form = TranslateForm()
        return render(request,'translation/translation.html',{'form':form,"translation":translation['translation']})
    
@csrf_protect
# @login_required(login_url='/login')
@require_http_methods(["POST"])
def feedback(request):
    form = TranslateForm()
    return render(request,'translation/translation.html',{'form':form})