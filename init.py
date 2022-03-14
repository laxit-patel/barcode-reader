from _thread import *
import threading
from webbrowser import get
import mysql.connector
import logging
from reader import getBarcode

logging.basicConfig(filename="reader.log")
logging.warning('Log Started')
logging.warning('Reader Started')

# start : DB Connection with
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  port = 3306, #for Mamp users
  database='test_barcode'
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM barcode_machine_masters where type='packing'")
myresult = mycursor.fetchall()
# End : DB Connection

# Init Thread
if __name__ == "__main__":

    for key,data in enumerate(myresult):
        temp = 'T' + str(key)
        temp = threading.Thread(target=getBarcode, args=(data,))
        temp.start()

    mydb.close()