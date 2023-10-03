from flask import Flask
import requests
from flask import Blueprint
import pymysql
 
# code for databse connection

# Set the database credentials
host = 'localhost'
port = 3306
user = 'myroo'
password = '19891104UMP'
database = 'prodtrack'

# Connect to the database
connection = pymysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)
