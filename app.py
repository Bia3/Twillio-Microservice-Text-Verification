from flask import Flask, request
from twilio.rest import Client
import json

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def send_code():
    try:
        if request.method == "POST":
            ret_data = json.dumps(request.data)
            # Your Account Sid and Auth Token from twilio.com/console
            # DANGER! This is insecure. See http://twil.io/secure
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

            # if ret_data.event:
            #     event = ret_data.event
            #     if event.data:
            #         payload_data = event.data
            #         if payload_data.new:
            #             user_activation_key = payload_data.new.user_activation_key
            #             return user_activation_key

            return request.data
        return "none"

    except Exception as e:
        return e


if __name__ == '__main__':
    app.run()
