# https://www.opentechguides.com/how-to/article/python/210/flask-mysql-crud.html

from getpass import getpass

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
app.config["MYSQL_DATABASE_USER"] = input("Username: ")
app.config["MYSQL_DATABASE_PASSWORD"] = getpass("Password: ")
app.config["MYSQL_DATABASE_DB"] = "sp500_db"
app.config["MYSQL_DATABASE_HOST"] = "localhost"

# init MySQL extension
mysql.init_app(app)

# Get all tickers being tracked in the DB
class Tickers(Resource):
    def get(self):
        """
        Get a list of all companies being tracked in the database
        """

        try:
            cnx = mysql.connect()
            cursor = cnx.cursor()

            cursor.execute("SHOW TABLES;")
            tickers = [i[0] for i in cursor.fetchall()]  # unpacking tuples

            response = jsonify(tickers)
            response.status_code = 200

        except Exception as e:
            print(e)
            response.status_code = 400

        finally:
            cursor.close()
            cnx.close()
            return response

    def post(self):
        """
        Add a new company to the database
        """

        try:
            cnx = mysql.connect()
            cursor = cnx.cursor()

            _ticker = request.form["ticker"]
            create_table = f"""
                CREATE TABLE {_ticker} (
                    High float(2),
                    Low float(2),
                    Open float(2),
                    Close float(2),
                    Volume int
                );
            """

            cursor.execute(create_table)
            cnx.commit()

            response = jsonify(message=f"Table for {_ticker} created successfully")
            response.status_code = 201

        except Exception as e:
            print(e)
            response = jsonify(message=f"Failed to create table for {_ticker}")
            response.status_code = 400

        finally:
            cursor.close()
            cnx.close()
            return response

    def delete(self):
        """
        Remove a company and its associated data from the database
        """

        try:
            cnx = mysql.connect()
            cursor = cnx.cursor()

            _ticker = request.form["ticker"]
            delete_table = f"""
                DROP TABLE {_ticker};
            """

            cursor.execute(delete_table)
            cnx.commit()

            response = jsonify(message=f"Table for {_ticker} deleted successfully")
            response.status_code = 200

        except Exception as e:
            print(e)
            response = jsonify(message=f"Failed to delete table for {_ticker}")
            response.status_code = 400

        finally:
            cursor.close()
            cnx.close()
            return response


# API resource routes
api.add_resource(Tickers, "/tickers", endpoint="tickers")


if __name__ == "__main__":
    app.run(debug=True)
