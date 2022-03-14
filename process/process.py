import mysql.connector
import socket
import time
import os
import logging

DB = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  port = 3306, #for Mamp users
  database='test_barcode'
) # start : DB Connection with

cursor = DB.cursor()
cursor.execute("SELECT id, ip, port, plant_id, line_id, machine_id from processing_master LIMIT 1")
process = cursor.fetchall()

logging.basicConfig(filename="dispatch.log")
logging.warning('Log Started')

pquery = "UPDATE processing_master SET pid = %s, status = '1' where id = '%s'"
pvalue = (os.getpid(),process[0][0])
cursor.execute(pquery,pvalue)
DB.commit()

try:
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object
    scanner.connect((process[0][1], int(process[0][2])))

    eq = "UPDATE processing_master SET status = 2 where id = %s"
    ev = (process[0][0],)
    cursor.execute(eq,ev)
    DB.commit()
    while True:
        time.sleep(0.4)
        
        res = scanner.recv(100).decode()

        if (len(res.strip())):
            try:
                tmp = res.split()
                for x in tmp:
                    db1 = DB.cursor()
                    db1query = "INSERT into raw_dispatch_masters(machine_id,plant_id,line_id,barcode) VALUES( %s,%s,%s,%s )"
                    db1value = (process[0][5],process[0][3],process[0][4],x)
                    db1.execute(db1query,db1value)
                    DB.commit()
                    # quit()
                    print('IP : ',process[0][1])
                    print('Barcode : ',x)
                    res = ''       
                    
            except mysql.connector.Error as e: # mysql exception
                print(str(e))
                DB.reconnect(attempts=10000, delay=10) #attempts 10000 times to reconnect with delay of 10 seconds
            
            finally:
                # closing database connection.
                if  DB.is_connected():
                    DB.close()
                    #reconnect database
                    DB.reconnect(attempts=10000)
        else:
            print('skipping')
    
except socket.error as e: #reading exception
    pquery = "UPDATE processing_master SET status = %s, error= %s where id = '%s'"
    pvalue = (3,"Could not connect !",process[0][0])
    cursor.execute(pquery,pvalue)
    DB.commit()