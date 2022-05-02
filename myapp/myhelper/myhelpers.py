import re
import json, requests
from urllib import response
from wsgiref import headers
from urllib.request import urlopen
import bcrypt
import os
from random import randint
import africastalking
import uuid

#User location
def userLocation():
    try:
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        user_data = json.load(response)
        return user_data
    except:
        return 'none'

#get authorization token
def fetch_auth_token():
    try:
        url = 'https://www.universal-tutorial.com/api/getaccesstoken'
        headers = {
            "Accept": "application/json",
            'api-token': 'dZ53GQV312pF3cHcOfEVr86dWrJrCOWW_j_IxUaZjsJuqfgCJZEQ6aShudFJ00dvtoY',
            "user-email": "madugbaemmanuel@gmail.com"
            }
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        return 'none'

 
#get countries
def countries():
    try:
        token = fetch_auth_token()
        auth_token = token['auth_token']
        url = 'https://www.universal-tutorial.com/api/countries'
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        return response.json()
    except:
        return 'none'

#State list
def user_state(country):
    try:
        token = fetch_auth_token()
        auth_token = token['auth_token']
        url = f'https://www.universal-tutorial.com/api/states/{country}'
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
        } 
        response = requests.get(url, headers=headers)
        return response.json()  
    except:
        return 'none'
    
    
def cities(state):
    try:
        token = fetch_auth_token()
        auth_token = token['auth_token']
        url = f'https://www.universal-tutorial.com/api/cities/{state}'
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
        } 
        response = requests.get(url, headers=headers)
        return response.json()  
    except:
        return 'none'
    

#hash password
def hashpassword (password):
    return bcrypt.hashpw(password, bcrypt.gensalt())

#check password
def checkpassword(password, hashedpassword):
    return bcrypt.checkpw(password, hashedpassword)

#Generate random number
def random_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


# function for sending SMS
def sendsms(telephone):
    code = random_digits(6)
    message=f'Your verification code is {code}'
    number = '+234{}'.format(telephone[1:] if telephone.startswith('0') else telephone)
    app_key = os.environ.get('AFRICA_TALK_API') 
    app_username= os.environ.get('AFRICA_TALK_USERNAME') # use 'sandbox' for development in the test environment
    
    # Initialize the SDK
    africastalking.initialize(app_username, app_key)

    # Initialize a service e.g. SMS
    sms = africastalking.SMS
    response = sms.send(message, [number])
    response['code'] = code
    return response

def verify_with_call(telephone):
    code = random_digits(6)
    number = '+234{}'.format(telephone[1:] if telephone.startswith('0') else telephone)
    app_key = os.environ.get('AFRICA_TALK_API')
    app_username = os.environ.get('AFRICA_TALK_USERNAME')

    # Initialize UUID
def get_uuid_id():
    return str(uuid.uuid4())