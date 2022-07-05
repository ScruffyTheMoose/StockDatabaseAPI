import getpass
from mysql.connector import connect, Error


# initializing connection to the SP500 database
try:
    cnx = connect(
        host="localhost",
        user=input("Username: "),
        password=getpass("Password: "),
        database="sp500_db",
    )
except Error as err:
    print(err)

cursor = cnx.cursor()
