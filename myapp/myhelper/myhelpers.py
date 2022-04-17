import re
import json
from urllib.request import urlopen
import bcrypt
import os
from random import randint
import africastalking

#User location
def userLocation():
    try:
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        user_data = json.load(response)
        return user_data
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