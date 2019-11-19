import jwt
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

                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                      from_='+12243061956',
                      body=ret_data['event']["data"]["new"]["user_activation_key"],
                      to=ret_data['event']["data"]["new"]["phone_number"]
                    )
                    return "{}".format({'success': message.sid})

        return "Forbidden", 403

    except Exception as e:
        return "{}".format({'Error': e.__str__()}), 500


if __name__ == '__main__':
    app.run()
