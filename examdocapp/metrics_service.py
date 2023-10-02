#user_service.py
from flask import Flask, request, redirect
from flask import Blueprint
import pymysql
import databasecon
import auth_service
import requests
import user_service
import urllib.parse

metrics_api = Blueprint('metrics_api', __name__)

#Entry point of the microservice
@metrics_api.route('/viewmetrics', methods=['POST'])
def view_metrics():
        print("good")
        gitusername=request.args.get("gitusername")
        apikey=request.args.get("apikey")
        key_status=auth_service.validate_key(gitusername,apikey)
        print(key_status)

        #call github api for metrics if key is valied
        if key_status==1:

            #Get total number of commits in a project as one metrics
            user_commits = requests.get('https://api.github.com/repos/manuja/LASMS/commits?author='+gitusername)
            no_of_user_commits=len(user_commits.json()) 
            print(no_of_user_commits) 

            #Get no of issues in a project as one metrics
            user_issues = requests.get('https://api.github.com/repos/manuja/LASMS/issues?assignee='+gitusername+'&state=open')
            no_of_user_issues=len(user_issues.json()) 
            print(no_of_user_issues) 

            #Get no of imoji icons
            user_comments = requests.get('https://api.github.com/repos/manuja/LASMS/issues?user='+gitusername)
            no_of_user_comments=user_comments.json()
            print('<pre>')
            total_imoji=0
            for x in range(2):
                total_imoji=total_imoji+no_of_user_comments[x]['reactions']['+1']
            #print(no_of_user_comments[0]['reactions']['hooray'])
            print(total_imoji)
            #print(no_of_user_comments[0]['reactions']['hooray'])

            #check exsistance of user in metrics table
            exsist_metrics=user_service.check_exsistance(gitusername)
            total_imoji_value=total_imoji

            if exsist_metrics==1 :
                
                #update the metrics table
                cursor = databasecon.connection.cursor()
                create_table_query = '''UPDATE tblusermetrics SET commits=(%s),issues=(%s),other=(%s)  WHERE user_id=(SELECT id FROM tbluser WHERE gitusername=(%s)) ;'''
                cursor.execute(create_table_query,(no_of_user_commits,no_of_user_issues,total_imoji_value,gitusername))
                userid=cursor.lastrowid
                databasecon.connection.commit()

                return f"Searched User: {gitusername} has {no_of_user_commits} of commits, {no_of_user_issues} of issues and {total_imoji_value} of Thumbsup Emoji. Based on the developer productivity calculation, {gitusername} has scored 79%"

            else : 
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

                return f"Searched User: {gitusername} has {no_of_user_commits} of commits, {no_of_user_issues} of issues and {total_imoji_value} of Thubsup Emoji. Based on the developer productivity calculation, {gitusername} has scored 79%"
        else:
            
            return redirect("/")

        
        