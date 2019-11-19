import jwt
from flask import Flask, request
from twilio.rest import Client
from os import environ, getenv
import json


app = Flask(__name__)
SECRET_KEY = getenv('SECRET_KEY')
API_KEY = getenv('API_KEY')


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, SECRET_KEY)
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

            account_sid = environ['TWILIO_ACCOUNT_SID']
            auth_token = environ['TWILIO_AUTH_TOKEN']
            client = Client(account_sid, auth_token)

            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
            if auth_token:
                if decode_auth_token(auth_token) == API_KEY:
                    return True
                    # account_sid = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                    # auth_token = 'your_auth_token'
                    # client = Client(account_sid, auth_token)
                    #
                    # message = client.messages.create(
                    #                               from_='+15017122661',
                    #                               body='body',
                    #                               to='+15558675310'
                    #                           )
                    #
                    # print(message.sid)
                    # return ret_data['event']

                    # if ret_data["event"]:
                    #     event = ret_data["event"]
                    #     if event["data"]:
                    #         payload_data = event["data"]
                    #         if payload_data["new"]:
                    #             new_data = payload_data["new"]
                    #             phone_number = new_data["phone_number"]
                    #             user_activation_key = new_data["user_activation_key"]
                    #             return "activation_key: {}\nphone: {}".format(user_activation_key, phone_number)
        return "none"

    except Exception as e:
        return {'Error': e.__str__()}


if __name__ == '__main__':
    app.run()
