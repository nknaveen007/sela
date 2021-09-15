import json
import os
from twilio.rest import Client
from decouple import config
import asyncio

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')
twilio_service = config('SERVICES_TWILIO')
client = Client(account_sid, auth_token)


def sendOtpHelper(number):
    print(number)
    try:
        verification = client.verify \
            .services(twilio_service) \
            .verifications \
            .create(to=number, channel='sms')
        print(verification.status)
        return {'Status': True, 'Message': 'OTP sent to your given number '+number}
    except Exception as e:
        print(e)
        return {'Status': False, 'Message': 'your number is not valid or something wrong'}


def verifyOtpHelper(number, code):
    print(number, code, 'in verify')
    try:
        verification_check = client.verify \
            .services(twilio_service) \
            .verification_checks \
            .create(to=number, code=code)
        print(verification_check.status, verification_check.valid, 'hii')

        return {'status': verification_check.status, 'valid': verification_check.valid}
    except:
        return{'status': False, 'valid': False}
