#metrics_service.py
from flask import Flask, request, redirect, jsonify
from flask import Blueprint
import pymysql
import databasecon
import auth_service
import requests
import user_service
import urllib.parse
import datetime
import random
import circuitbreaker

metrics_api = Blueprint('metrics_api', __name__)
breaker = circuitbreaker.CircuitBreaker()

#Entry point of the microservice
@metrics_api.route('/update_metrics', methods=['POST'])
def update_metrics():
        print("good")
        gitusername=request.args.get("gitusername")
        apikey=request.args.get("apikey")
        key_status=auth_service.validate_key(gitusername,apikey)
        print(key_status)
        

        #call github api for metrics if key is valied
        if key_status==1:

            #Get total number of commits in a project as one metrics
            
            url='https://api.github.com/repos/manuja/LASMS/commits?author='

            #invoke the circiut breaker
            user_commits = breaker.execute(gitusername,url)

            #return user_commits

            if (user_commits) == "500" :
                return "Github api handshake could not be established"
            elif (user_commits) == "424" :
                return "Circuit Breaker on !!!"
            else:
                no_of_user_commits=len(user_commits)
            
            
            # #Get no of issues in a project as one metrics

            url_issues = 'https://api.github.com/repos/manuja/LASMS/issues?assignee='
            user_issues = breaker.execute(gitusername,url_issues)

            if (user_issues) == "500" :
                return "Github api handshake could not be established"
            elif (user_issues) == "424" :
                return "Circuit Breaker on !!!"
            else:
                no_of_user_issues=len(user_issues)
             

            #Get no of imoji icons

            url_imoji = 'https://api.github.com/repos/manuja/LASMS/issues?user='
            user_imoji = breaker.execute(gitusername,url_imoji)

            if (user_imoji) == "500" :
                return "Github api handshake could not be established"
            elif (user_imoji) == "424" :
                return "Circuit Breaker on !!!"
            else:
                no_of_user_comments=len(user_imoji)

            
                no_of_user_comments=user_imoji
                total_imoji=0
                for x in range(2):
                    total_imoji=total_imoji+no_of_user_comments[x]['reactions']['+1']
                #print(no_of_user_comments[0]['reactions']['hooray'])
                print(total_imoji)
                #print(no_of_user_comments[0]['reactions']['hooray'])

                #check exsistance of user in metrics table
                #exsist_metrics=user_service.check_exsistance(gitusername)
                total_imoji_value=total_imoji

         
            now = random. random()

            #update the metrics table
            cursor = databasecon.connection.cursor()
            update_table_query = '''UPDATE tblusermetrics SET commits=(%s),issues=(%s),other=(%s),record_log_time=(%s)  WHERE user_id=(SELECT id FROM tbluser WHERE gitusername=(%s)) ;'''
            cursor.execute(update_table_query,(no_of_user_commits,no_of_user_issues,total_imoji_value,now,gitusername))
            # Check the affected rows count
            affected_rows = cursor.rowcount
            databasecon.connection.commit()

            print("gyyyy")
            print(affected_rows)

            if affected_rows == 0:
                print("I am here no worries")
                
                print(no_of_user_commits)
                print(no_of_user_issues)
                print(total_imoji_value)
                gituserid=user_service.getuserid(gitusername)
                print(gituserid)
                #insert the metrics table
                cursorinsert = databasecon.connection.cursor()
                create_table_query = '''INSERT INTO tblusermetrics (user_id,commits, issues, other) VALUES (%s,%s,%s,%s);'''
                cursorinsert.execute(create_table_query,(gituserid,no_of_user_commits,no_of_user_issues,total_imoji_value))
                databasecon.connection.commit()

                return f"Searched User: {gitusername} has {no_of_user_commits} of commits, {no_of_user_issues} of issues and {total_imoji_value} of Thubsup Emoji. Record updated successfully!!!" 
            else:
        
                return f"Searched User: {gitusername} has {no_of_user_commits} of commits, {no_of_user_issues} of issues and {total_imoji_value} of Thumbsup Emoji.Record updated successfully!!! "


                
        else:
            
            return redirect("/")

        
        