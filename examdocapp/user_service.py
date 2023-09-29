#user_service.py
from flask import Flask, request, redirect

from flask import Blueprint

user_api = Blueprint('user_api', __name__)

#Entry point of the microservice
@user_api.route('/exsistance/<username>', methods=['GET'])
def check_exsistance(username):

        return f"Exsistance Process Goes here {username}"
    
