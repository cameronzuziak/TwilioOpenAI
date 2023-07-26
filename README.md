# **TwilioOpenAI**
A production ready project that let's user talk to ChatGPT over text message. 

## Overview 
This project allows you to interact with OpenAI GPT models over SMS via Twilio's API first SMS/MMS services. Utilizing SMS/MMS as a chat interface makes ChatGPT truly universal and crossplatform. You can now interact with ChatGPT on non-smart phones with T9 texting. However, there are a few things you need beforehand in order to get started.

## Prerequisites
1. OpenAI API Key and Secret Key  
    - You can find out more about getting OpenAI API keys [here](https://openai.com/blog/openai-api)
2. Twilio API Key
3. Twilio Secret Key
4. A Twilio MMS Programmable Phone Number
   - Get started with a free trial account for Twilio [here](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account)
5. A machine/environment with docker compose installed
6. A public domain name, and a TLS/SSL cert for that domain
   - This is important for verifying incoming requests with Twilio's auth server which I'll go over later, but you can use ngrok and local host to get started too.

## Set Up
1. Once you've set up your twilio account and purchased a number, configure the web hook for that number in the twilio console to point to https://{your_domain}/api/chat for inbound messages, for more info look [here](https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python#configure-your-webhook-url)
2. Edit the '.env' file and fill in the corresponding variables with your api keys and data. Note that ORG_ID for OpenAI is only currently needed for GPT4 models. GPT3.5-turbo does not require it.
3. 



### Disclaimer
No Professional Association - This Software is an open-source application developed by Cameron Zuziak. I want to make it clear that the Software is not professionally associated with, endorsed, or sponsored by Twilio or OpenAI ("Providers"). I have developed this Software independently and all interactions or communication facilitated by the Software are solely your responsibility.
