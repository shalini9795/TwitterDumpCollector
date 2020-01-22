import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText

from flask import Flask, render_template, request, jsonify, make_response, json
from flask_mail import Mail,Message
import gunicorn

import TweetsDumpGen

app = Flask(__name__)


with open('details.json') as f:
    data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tweets')
def play():
    global name
    name = request.args.get('username')
    # email=request.args.get('email')
    if name ==None or name==" " or not name:
        return render_template('index.html')
    a=TweetsDumpGen.get_all_tweets(name.lstrip().rstrip().strip())

    return a


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(threaded=True, port=5000)
    name=''