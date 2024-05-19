from dotenv import load_dotenv
from requests import RequestException
import requests
import os 
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()
CREDENTIALS = {'username':os.getenv('API_AI_USER'),'password':os.getenv('API_AI_PWD')}

def get_access_token(login_url:str):
    """
    Make a request to get the access token 
    """
    
    try:
        response = requests.post(login_url,data=CREDENTIALS)
        if response.status_code == 200:
            logger.info(f"[{datetime.now().strftime('%H:%M:%S')}] : Successfully retrieved the JWT from the API ")
            return response.json()
        else:
            logger.error(f"[{datetime.now().strftime('%H:%M:%S')}] : Could not get the JWT from the API. Status_code = {response.status_code}  ")
            return False
    except RequestException as e:
        logger.error(f"[{datetime.now().strftime('%H:%M:%S')}] : Error while making the request to get thr JWT. \n {str(e)}")
        return False

def call_api_ai(payload:dict,api_url:str,login_url:str,expected_status_code:int=200,attempts:int=3):
    """
    Make a POST request to the model API 
    """
    
    # 1. Get access token 
    access_token = get_access_token(login_url)
    # 2. Connect
    for attempt in range(attempts) :
        if access_token:
            headers = {"Authorization": f"Bearer {access_token['access_token']}"}
            try:
                req = requests.post(api_url,json=payload,headers=headers)
                if req.status_code == expected_status_code :
                    return req.json()
                else: 
                    return False
            except RequestException as e:
                if attempt == attempts:
                    return  False
                # get new token
                access_token = get_access_token(login_url)
                continue
        else:
            if attempt == attempts:
                return  False
            access_token = get_access_token(login_url)
            continue

