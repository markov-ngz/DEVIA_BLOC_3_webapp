from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def metrics(request):
    response = HttpResponse("METRICS ",content_type='text/plain')
    # response.write(generate_latest())
    return response

