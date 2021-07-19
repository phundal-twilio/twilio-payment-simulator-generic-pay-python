from flask import (
    Flask,
    jsonify,
    request
)
import uuid
from datetime import datetime
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from pprint import pprint


app = Flask(__name__)
auth = HTTPBasicAuth()

# Basic Test
# curl -H "Content-Type: application/json" --data @pay.json https://foo:bar@41ccedcc4469.ngrok.io/charge

# Test to mimic post from pay connector
# curl -X 'POST' 'https://foo:bar@b89a9d561bab.ngrok.io/charge' -H 'user-agent: AHC/2.1'  -H 'authorization: Basic Zm9vOmJhcg==' -H 'content-type: ' --data @pay.json


users = {
    "foo": generate_password_hash("bar"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    response = "<h2>Use /charge or /tokenize endpoints to test </h2>"
    return response

@app.route('/charge', methods=['POST'])
@auth.login_required
def charge():
    if request.method == 'POST':
      post_data = request.get_json(force=True)
    else:
      return "<h1> These are not the droids you are looking for </h1>"
    pprint(post_data)

    # retrieve critical elements of posted data for validation
    transaction_id = post_data['transaction_id']
    firstFour = post_data['cardnumber'][0:4]
    lastFour = post_data['cardnumber'][12:16]
    cardExp = post_data['expiry_year'] + post_data['expiry_month']
    description = post_data['description']

    # Build current date time string to validate
    now = datetime.now()
    twoDigitYear = now.strftime("%y")
    twoDigitMonth = now.strftime("%m")
    minExpiry = twoDigitYear + twoDigitMonth
    validFirstFour = ['5555','4111']
    validLastFour = ['4444', '1111']

    #build response
    response = {}
    response['charge_id'] = str(uuid.uuid4())
    if float(minExpiry) < float(cardExp):
        if firstFour in validFirstFour:
            if lastFour in validLastFour:
                response['error_code'] = None
                response['error_message'] = None
            else:
                response['error_code'] = 'errorFunds001'
                response['error_message'] = 'Funds not available.'
        else:
            response['error_code'] = 'invalid001'
            response['error_message'] = 'Card number not accepted.'

    else:
        response['error_code'] = 'expired001'
        response['error_message'] = 'Expired card.'


    return jsonify(response)

@app.route('/tokenize', methods=['POST'])
def tokenize():
    if request.method == 'POST':
      post_data = request.get_json(force=True)
    else:
      return "<h1> These are not the droids you are looking for </h1>"
    pprint(post_data)

    transaction_id = post_data['transaction_id']
    firstFour = post_data['cardnumber'][0:3]
    lastFour = post_data['cardnumber'][12:15]
    cardExp = post_data['expiry_year'] + post_data['expiry_month']
    description = post_data['description']

    # Build current date time string to validate
    now = datetime.now()
    twoDigitYear = now.strftime("%y")
    twoDigitMonth = now.strftime("%m")
    minExpiry = twoDigitYear + twoDigitMonth
    validFirstFour = ['5555','4111']
    validLastFour = ['4444', '1111']

    #build response
    response = {}
    response['token_id'] = str(uuid.uuid4())
    if float(minExpiry) < float(cardExp):
        if firstFour in validFirstFour:
            if lastFour in validLastFour:
                response['error_code'] = None
                response['error_message'] = None
            else:
                response['error_code'] = 'errorFunds001'
                response['error_message'] = 'Funds not available.'
        else:
            response['error_code'] = 'invalid001'
            response['error_message'] = 'Card number not valid.'

    else:
        response['error_code'] = 'expired001'
        response['error_message'] = 'Expired card.'

    return jsonify(response)


if __name__ == '__main__':
    app.run(port = '8081', debug = True)
