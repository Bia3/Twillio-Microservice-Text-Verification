import jwt
import re
from flask import Flask, request
from base64 import b64decode
from twilio.rest import Client
import os
import json

app = Flask(__name__)
SECRET_KEY = os.getenv('SECRET_KEY', '')
API_KEY = os.getenv('API_KEY', '')
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
twillio_token = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER_ELEVEN_US = re.compile(r'\+1[0-9]{10}')
PHONE_NUMBER_US_NO_SYMBOLS = re.compile(r'[0-9]{10}')
PHONE_NUMBER_US_SYMBOLS = re.compile(r'((\+|)1|\(|(\+|)1|)( |)(\(|)[0-9]{3}(\)|-| )( |)[0-9]{3}(-|)[0-9]{4}')
PHONE_NUMBER_ALL_FIVES = re.compile(r'((\+|)1|\(|(\+|)1 \(|)555(\) |)555(\-|)5555')
PHONE_NUMBER_PLUS = re.compile(r'^\+[0-9]+')


def format_number(my_number):
    if not PHONE_NUMBER_ELEVEN_US.match(my_number):
        if not PHONE_NUMBER_ALL_FIVES.match(my_number):
            if PHONE_NUMBER_US_SYMBOLS.match(my_number):
                my_number = my_number.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
            if not PHONE_NUMBER_ELEVEN_US.match(my_number):
                my_number = "+1{}".format(my_number)
                return my_number
            if my_number.__contains__(' '):
                my_number = my_number.replace(' ', '')
            if my_number.__contains__('('):
                my_number = my_number.replace(' ', '')
            if my_number.__contains__(')'):
                my_number = my_number.replace(' ', '')
            if my_number.__contains__('-'):
                my_number = my_number.replace(' ', '')
            if not PHONE_NUMBER_PLUS.match(my_number):
                my_number = "+{}".format(my_number)
            return my_number
        return 0
    return my_number


def decode_auth_token(my_token):
    """
    Decodes the auth token
    :param my_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(my_token, SECRET_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


@app.route('/', methods=["GET", "POST"])
def send_code():
    try:
        if request.method == "POST":
            ret_data = json.loads(request.data.decode('utf8'))
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = b64decode(auth_header)
            else:
                auth_token = ''
            if auth_token:
                if decode_auth_token(auth_token) == API_KEY:
                    client = Client(account_sid, twillio_token)
                    message_format = request.headers.get('MessageFormatter')
                    phone_number_to = format_number(ret_data['event']["data"]["new"]["phone_number"])
                    phone_number_from = format_number(request.headers.get('From'))
                    activation_key = ret_data['event']["data"]["new"]["user_activation_key"]
                    message_body = message_format.format(activation_key)

                    # return "{}".format(True)
                    message = client.messages.create(
                      from_=phone_number_from,
                      body=message_body,
                      to=phone_number_to
                    )
                    return "{}".format({'success': message.sid})

        return "Forbidden", 403

    except Exception as e:
        return "{}".format({'Error': e.__str__()}), 500


if __name__ == '__main__':
    app.run()
