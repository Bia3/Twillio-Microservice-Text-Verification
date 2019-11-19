from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def send_code():
    try:
        if request.method == "POST":
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
            return request.form
        return "none"

    except Exception as e:
        return 'Error'


if __name__ == '__main__':
    app.run()
