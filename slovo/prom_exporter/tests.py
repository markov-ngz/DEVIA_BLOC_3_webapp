from django.test import TestCase , Client
import os 
import base64
from pprint import pprint

# Create your tests here.
class MetricsTest(TestCase):

    c = Client(enforce_csrf_checks=False)
    pwd = os.getenv("PROMETHEUS_PASSWORD")
    username = os.getenv("PROMETHEUS_USERNAME")

    def test_metrics_method(self):
        response = self.c.post("/metrics/")
        assert response.status_code == 405

    def test_metrics_auth(self):
        basic_auth_str=  self.username+":"+self.pwd
        basic_auth = base64.b64encode(basic_auth_str.encode())
        headers = {"Authorization":"Basic %s" % basic_auth.decode()}
        response  = self.c.get("/metrics/",headers=headers)
        assert response.status_code == 200 

