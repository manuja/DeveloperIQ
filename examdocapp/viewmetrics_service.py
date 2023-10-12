#viewmetrics_service.py
import re
from flask import Flask, request, redirect
from flask import Blueprint
import pymysql
import databasecon
import auth_service
import requests
import user_service
import urllib.parse
import datetime
import random

view_metrics_api = Blueprint('view_metrics_api', __name__)

#Entry point of the microservice
@view_metrics_api.route('/view_metrics', methods=['POST'])
def view_metrics():
        print("good")
        gitusername=request.args.get("gitusername")
        apikey=request.args.get("apikey")
        key_status=auth_service.validate_key(gitusername,apikey)
        print(key_status)

        #call github api for metrics if key is valied
        if key_status==1:

            # Create a cursor object
            cursor = databasecon.connection.cursor()
            # Execute a SQL query
            query = """SELECT * FROM tblusermetrics WHERE user_id=(SELECT id FROM tbluser WHERE gitusername=(%s))"""
            tuple1 = (gitusername)
            cursor.execute(query, tuple1)

            # Fetch the results
            results = cursor.fetchall()

            for x in results:
                print(x[0])
            
            #calculate the weighted average of each user
            weighted_average= ((x[1]*3)+(x[2]*2)+(x[3]*1)/6)
            

            return f"Searched User Is: {gitusername} has {x[2]} of commits, {x[3]} of issues and {x[4]} of Thumbsup Emoji. Based on the developer productivity calculation, {gitusername} has scored {weighted_average} "


            
        else:
            
            return redirect("/")

        
        