#auth_service.py
from flask import Flask, request, redirect

from flask import Blueprint

auth_api = Blueprint('auth_api', __name__)

#Entry point of the microservice
@auth_api.route('/authe', methods=['POST'])
def authenticate():

    username = request.args.get('uname')
    password = request.args.get('pword')
    if username=="manuja" and password=="123":
        print("Auth Success")
        return redirect("/exsistance/"+username)
    else :
        return redirect("/")
    
