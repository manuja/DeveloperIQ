#user_service.py
from flask import Flask, request, redirect
from flask import Blueprint
import pymysql
import databasecon

user_api = Blueprint('user_api', __name__)

#Entry point of the microservice
@user_api.route('/exsistance/<githubuser>', methods=['GET'])
def check_exsistance(githubuser):

        # Create a cursor object
        cursor = databasecon.connection.cursor()
        # Execute a SQL query
        query = """SELECT COUNT(*) FROM (SELECT um.user_id FROM tblusermetrics AS um LEFT JOIN tbluser AS u ON um.user_id=u.id  WHERE u.username=%s) AS tbl"""
        tuple1 = (githubuser)
        cursor.execute(query, tuple1)

        # Fetch the results
        results = cursor.fetchall()

        # Print the results
        record_count=results[-1][-1]

        # Close the cursor and connection
        cursor.close()
        databasecon.connection.close()

        return redirect("/exsistance/"+record_count)
