# app.py

from flask import Flask, jsonify, redirect
from product_service import product_api
from auth_service import auth_api
from user_service import user_api

app = Flask(__name__)

app.register_blueprint(product_api)
app.register_blueprint(auth_api)
app.register_blueprint(user_api)

@app.route('/')
def hello_world():

    return "Please complete the auth process"

if __name__ == '__main__':
    app.run(host='0.0.0.0')