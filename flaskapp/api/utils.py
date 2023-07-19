# imports
from config import TW_API_KEY, TW_SEC_API_KEY, TWILIO_NUMBER, ORG_ID, OPEN_AI_KEY
import openai
from twilio.rest import Client
from twilio.request_validator import RequestValidator
from flask import abort, request
from functools import wraps
import os
import json


# configure openai, org id is optional for gpt-3.5-turbo
# but might be needed for newer models
openai.organization = ORG_ID
openai.api_key = OPEN_AI_KEY


# function to chat with OpenAI
def chat(messages):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return(completion.choices[0].message["content"])


# function to send sms
def sms_send(text, client_phone):
    Client(TW_API_KEY, TW_SEC_API_KEY).messages.create(body=text,from_=TWILIO_NUMBER,to=client_phone)


# decorator to validate incoming twilio requests
def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(TW_SEC_API_KEY)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            # because the request was proxied by nginx, the url is http, so we need to replace it with https
            str(request.url).replace('http','https'),
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        if request_valid:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function

