from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from prometheus_client import Counter, generate_latest , CollectorRegistry , Histogram
import base64 , os

registry = CollectorRegistry()
NAMESPACE = "slovo" 

COUNT_REQ = Counter('http_requests_total', 'Total number of HTTP requests',namespace=NAMESPACE, registry=registry)
COUNT_HOME = Counter('core_requests_home', '/ number of HTTP requests',namespace=NAMESPACE, registry=registry)
COUNT_LOGOUT =  Counter('core_requests_logout', '/logout number of HTTP requests',namespace=NAMESPACE, registry=registry)
COUNT_SIGNUP =  Counter('core_requests_signup', '/signup number of HTTP requests',namespace=NAMESPACE, registry=registry)
COUNT_TRANSLATION =  Counter('translation_requests_translation', '/translation number of HTTP requests',namespace=NAMESPACE, registry=registry)
COUNT_FEEDBACK =  Counter('translation_requests_feedback', 'Total number of feedbacks',namespace=NAMESPACE, registry=registry)
COUNT_POSITIVE =  Counter('translation_feedback_positive', 'Total number of positive feedback',namespace=NAMESPACE, registry=registry)
COUNT_NEGATIVE =  Counter('translation_feedback_negative', 'Total number of negative feedback',namespace=NAMESPACE, registry=registry)
COUNT_AUTHENTICATION = Counter('translation_authentication_to_api_ai', 'Total number of authentication done',namespace=NAMESPACE, registry=registry)
COUNT_REQ_FAILED = Counter('translation_failed_req_to_api_ai', 'Total number of request that failed to the API',namespace=NAMESPACE, registry=registry)
TIME_TRANSLATION =  Histogram('translation_processing_seconds', 'Time spent processing a translation', namespace=NAMESPACE, registry=registry)
SIZE_BYTES_IN = Histogram('translation_size_bytes_in','In Request size (bytes)',namespace=NAMESPACE, registry=registry)
SIZE_BYTES_OUT = Histogram('translation_size_bytes_out',' Out Request size (bytes)',namespace=NAMESPACE, registry=registry)
SIZE_BYTES_GEN= Histogram('translation_size_bytes_gen','Generated Request size (bytes)',namespace=NAMESPACE, registry=registry)

PROMETHEUS_PASSWORD = os.getenv("PROMETHEUS_PASSWORD")
PROMETHEUS_USERNAME = os.getenv("PROMETHEUS_USERNAME")

@require_http_methods(["GET"])
def metrics(request):
    if 'Authorization' in request.headers:
        basic_auth = request.headers['Authorization'][6:]
        str_basic_auth = base64.b64decode(basic_auth).decode("utf-8")
        username, password = str_basic_auth.split(":")
        if username == PROMETHEUS_USERNAME and password == PROMETHEUS_PASSWORD:
            response = HttpResponse(content_type='text/plain')
            response.write(generate_latest(registry))
            return response
    response = HttpResponse()
    response.status_code = 404 
    return response

