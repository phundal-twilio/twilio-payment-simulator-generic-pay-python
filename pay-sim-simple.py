from flask import (
    Flask,
    request,
    jsonify
)
import uuid
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from pprint import pprint


app = Flask(__name__)
auth = HTTPBasicAuth()

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
      return "<h1> Error, no POST data </h1>"
    # Pretty print the data
    pprint(post_data)

    #build valid sample response
    response = {}
    response['charge_id'] = str(uuid.uuid4())
    response['error_code'] = None
    response['error_message'] = None

    return jsonify(response)

@app.route('/tokenize', methods=['POST'])
def tokenize():
    if request.method == 'POST':
      post_data = request.get_json(force=True)
    else:
      return "<h1> Error, no POST data </h1>"
    # Pretty print the data
    pprint(post_data)

    #build valid sample response
    response = {}
    response['token_id'] = str(uuid.uuid4())
    response['error_code'] = None
    response['error_message'] = None

    return jsonify(response)


if __name__ == '__main__':
    app.run(port = '8081', debug = True)
