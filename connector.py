# https://www.opentechguides.com/how-to/article/python/210/flask-mysql-crud.html

from getpass import getpass, getuser

from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api

# init flask instance
app = Flask(__name__)

# init MySQL instance
mysql = MySQL()

# init RESTful API
api = Api(app)

# setting DB credentials
app.config["MYSQL_DATABASE_USER"] = getuser("Username: ")
app.config["MYSQL_DATABASE_PASSWORD"] = getpass("Password: ")
app.config["MYSQL_DATABASE_DB"] = "sp500_db"
app.config["MYSQL_DATABASE_HOST"] = "localhost"

# init MySQL extension
mysql.init_app(app)
