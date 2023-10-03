#auth_service.py
from flask import Flask, request, redirect
import uuid
from flask import Blueprint
import databasecon

auth_api = Blueprint('auth_api', __name__)

#Entry point of the microservice
@auth_api.route('/authe', methods=['POST'])
def authenticate():

    username = request.args.get('uname')
    password = request.args.get('pword')
    githubuser = request.args.get('gituser')
    if username=="manuja" and password=="Bd#19911225A":
        authkey = uuid.uuid1()
        print("I am here 01")

        #check the exsistance of the gituser
        cursor = databasecon.connection.cursor()
        query = """SELECT COUNT(*) FROM tbluser WHERE gitusername=%s"""
        tuple1 = (githubuser)
        cursor.execute(query, tuple1)
        results = cursor.fetchall()
        record_count=results[-1][-1]
        # cursor.close()
        # databasecon.connection.close()

        print(record_count)
        print("I am here 02")
        if(record_count>0):
            #Update the api tocken for exsisting user  
            cursor = databasecon.connection.cursor()
            authkeyval= str(authkey)
            create_table_query = '''UPDATE tblauth SET authkey=(%s) WHERE userid=(SELECT id FROM tbluser WHERE gitusername=(%s));'''
            cursor.execute(create_table_query,(authkeyval,githubuser))
            userid=cursor.lastrowid
            databasecon.connection.commit()
            print("I am here 03")
            # cursor.close()
            # databasecon.connection.close()
        else:  
            # Insert into user table
            cursor = databasecon.connection.cursor()
            create_table_query = '''INSERT INTO tbluser (gitusername) VALUES (%s);'''
            cursor.execute(create_table_query,(githubuser))
            userid=cursor.lastrowid
            authkeyval= str(authkey)
            databasecon.connection.commit()
            print("I am here 04")
            # Intert into auth table
            cursor_auth = databasecon.connection.cursor()
            create_table_query_auth = '''INSERT INTO tblauth (userid,authkey) VALUES (%s, %s);'''
            cursor_auth.execute(create_table_query_auth,(userid,authkeyval))
            databasecon.connection.commit()
            print("I am here 05")
            # cursor_auth.close()
            # databasecon.connection.close()

        return str(authkey) 
    else :
        return redirect("/")
    
    #Check the validity of the apikey
def validate_key(gitusername,apikey):

        # Create a cursor object
        cursor = databasecon.connection.cursor()
        # Execute a SQL query
        query = """SELECT COUNT(*) FROM tblauth WHERE userid=(SELECT id FROM tbluser WHERE gitusername=(%s)) AND authkey=(%s)"""
        tuple1 = (gitusername,apikey)
        cursor.execute(query, tuple1)

        # Fetch the results
        results = cursor.fetchall()

        # Print the results
        record_count=results[-1][-1]
        if record_count>0:
            status=1
        else:
            status=0


        return status

        
        
