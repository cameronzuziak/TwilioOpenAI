import os

#twilio keys
TW_API_KEY = os.environ.get('TW_API_KEY')
TW_SEC_API_KEY = os.environ.get('TW_SEC_API_KEY')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

#openai keys
OPEN_AI_KEY = os.environ.get('OPEN_AI_KEY')
ORG_ID = os.environ.get('ORG_ID')

#flask base config object
class BaseConfig():
    SECRET_KEY = os.environ.get('SECRET_KEY')

