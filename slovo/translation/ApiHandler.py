from dotenv import load_dotenv
from requests import RequestException
import requests
import os 
import logging
from datetime import datetime
from prom_exporter.views import COUNT_REQ_FAILED , COUNT_AUTHENTICATION

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()
CREDENTIALS = {'username':os.getenv('API_AI_USER'),'password':os.getenv('API_AI_PWD')}


class ApiHandler():
    pass