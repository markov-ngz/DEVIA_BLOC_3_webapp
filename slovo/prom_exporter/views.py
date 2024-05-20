from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from prometheus_client import Counter, generate_latest , CollectorRegistry

registry = CollectorRegistry()
NAMESPACE = "slovo" 

COUNT_REQ = Counter('http_requests_total', 'Total number of HTTP requests',namespace=NAMESPACE, registry=registry)

@require_http_methods(["GET"])
def metrics(request):
    response = HttpResponse("METRICS ",content_type='text/plain')
    response.write(generate_latest(registry))
    return response

