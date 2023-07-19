# imports
from config import BaseConfig
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from utils import sms_send, chat, validate_twilio_request
import redis
import traceback
import pickle
from datetime import datetime

# config app
app = Flask(__name__)
app.config.from_object(BaseConfig)

# create redis connection
r = redis.StrictRedis(host='redis',port=6379,db=0)

# hardcoded numbers
approved_numbers = [
    '+19496834700'
]

# route to echo data for testing
@app.route("/api/echo", methods=['POST'])
def echo_data():
    data = request.get_json()
    return jsonify(data),200


# route to handle incoming sms messages
@app.route("/api/chat", methods=['POST'])
@validate_twilio_request
def sms_reply():
    # timer to see if response took longer than 15 sec
    start_time = datetime.now()
    try:

        # get arguements
        body = request.values.get('Body', None)

        # get from number
        from_number = request.values.get('From')

        # check if number is approved
        if from_number not in approved_numbers:
            return jsonify({"msg":"access denied"}),401


        # check redis for previous context using from_number as key, and handle cache miss
        if not (r.exists(str(from_number))):
            msg = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": str(body)}
            ]
            r.set(str(from_number), value=pickle.dumps(msg))
        
        # if cache hit, grab conversation context
        else: 
            msg = pickle.loads(r.get(str(from_number)))
            msg.append({"role": "user", "content": str(body)})

        # pass conversation context to gpt
        text = chat(messages=msg)

        # append response to conversation context
        msg.append({"role":"system","content":str(text)})
        
        # update redis with conversation context
        pickled_list = pickle.dumps(msg)
        r.set(str(from_number), value=pickled_list) 

        # remove context after 24hrs to save memory
        r.expire(str(from_number),1440)


        # Sometimes when OpenAI API has a lot of traffic 
        # and/or the model context is large, it can take a while to generate a response.
        # Incoming Twilio requests time out after 15 seconds, 
        # so we need to send the message response manually if it takes longer than that.
        if(datetime.now() - start_time).seconds < 14.5:

            # create TwilML messaging response
            resp = MessagingResponse()            
            resp.message(str(text))
            return str(resp)
    
        else:
            # send response via sms
            sms_send(str(text),from_number)

            # even tho request timed out, 
            # Flask will throw an error if we don't return something
            return '',200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"msg":"server error"}),500



# start app
if __name__ == "__main__":
    # run app
    app.run(host='0.0.0.0', debug=False)

