from _thread import *
import threading
import mysql.connector
import socket
import time

con = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  port = 3306, #for Mamp users
  database='barcode'
) # start : DB Connection with

cursor = con.cursor()
cursor.execute("SELECT ip_address, port, machine_id, plant_id, line_id FROM barcode_machine_masters where type = 'dispatch' ")
barcode = cursor.fetchall()

# Read Barcode
def Reader(row):
    try:
        scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket object
        scanner.connect((row[0], int(row[1])))

        while True:
            time.sleep(0.4)
            
            res = scanner.recv(1024).decode('utf-8')
            
            if (len(res.strip())):      
                try:    
                    db1 = con.cursor()
                    db1query = "INSERT into raw_dispatch_masters(machine_id,plant_id,line_id,barcode) VALUES( %s,'%s','%s',%s )"
                    db1value = (row[0],row[4],row[5],res.strip())
                    db1.execute(db1query,db1value)
                    con.commit()
                    print("Dispatch Entry : ", res  + " @ " +row[2])
                    res = ''       
                        
                except mysql.connector.Error as e: # mysql exception
                    print(str(e))
                    con.reconnect(attempts=10000, delay=10) #attempts 10000 times to reconnect with delay of 10 seconds
                
                finally:
                    # closing database connection.
                    if con.is_connected():
                        con.close()
                        #reconnect database
                        con.reconnect(attempts=10000)
            else:
                print('skipping')
        
    except socket.error as e: #reading exception
        print(str(e))

# Init Thread
if __name__ == "__main__":

    for key,data in enumerate(barcode):
        temp = 'T' + str(key)
        temp = threading.Thread(target=Reader, args=(data,))
        temp.start()

    con.close()