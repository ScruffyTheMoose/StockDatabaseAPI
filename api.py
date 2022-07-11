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
            data = {"tickers": tickers}

            response = jsonify(data)
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
                    date VARCHAR(10),
                    High float(2),
                    Low float(2),
                    Open float(2),
                    Close float(2),
                    Volume int(12)
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


class CompanyData(Resource):
    def get(self):
        try:
            cnx = mysql.connect()
            cursor = cnx.cursor()

            _ticker = request.args["ticker"]
            _start_date = request.args["start_date"]
            _end_date = request.args["end_date"]

            get_data = f"""
                SELECT * FROM {_ticker} WHERE date >= '{_start_date}' AND date <= '{_end_date}';
            """

            cursor.execute(get_data)
            company_data = cursor.fetchall()
            data = {"data": company_data}

            response = jsonify(data)
            response.status_code = 200

        except Exception as e:
            print(e)
            response = jsonify(
                message=f"Failed to retrieve data for {_ticker} between dates {_start_date} and {_end_date}"
            )
            response.status_code = 400

        finally:
            cursor.close()
            cnx.close()
            return response

    def post(self):
        try:
            cnx = mysql.connect()
            cursor = cnx.cursor()

            _ticker = request.form["ticker"]
            _date = request.form["date"]
            _high = request.form["high"]
            _low = request.form["low"]
            _open = request.form["open"]
            _close = request.form["close"]
            _volume = request.form["volume"]

            add_price_data = f"""
                INSERT INTO {_ticker}(date, high, low, open, close, volume) VALUES ({_date}, {_high}, {_low}, {_open}, {_close}, {_volume});
            """

            cursor.execute(add_price_data)
            cnx.commit()

            response = jsonify(
                message=f"Successfully inserted price data for {_ticker} for date {_date}"
            )
            response.status_code = 200

        except Exception as e:
            print(e)
            response = jsonify(
                message=f"Failed to insert price data for {_ticker} for date {_date}"
            )
            response.status_code = 400

        finally:
            cursor.close()
            cnx.close()
            return response

    def delete(self):
        try:
            cnx = mysql.connect()
            cursor = cnx.cursor()

            _ticker = request.form["ticker"]
            _start_date = request.form["start_date"]
            _end_date = request.form["end_date"]

            delete_data = f"""
                DELETE FROM {_ticker} WHERE date >= '{_start_date}'AND date <= '{_end_date}';
            """

            cursor.execute(delete_data)
            cnx.commit()

            response = jsonify(
                message=f"Successfully deleted price data for {_ticker} between dates {_start_date} and {_end_date}"
            )
            response.status_code = 200

        except Exception as e:
            print(e)
            response = jsonify(
                message=f"Failed to delete price data for {_ticker} between dates {_start_date} and {_end_date}"
            )
            response.status_code = 400

        finally:
            cursor.close()
            cnx.close()
            return response


# API resource routes
api.add_resource(Tickers, "/tickers", endpoint="tickers")
api.add_resource(CompanyData, "/data", endpoint="data")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
