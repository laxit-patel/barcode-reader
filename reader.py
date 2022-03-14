import socket
import time
from datetime import datetime
import mysql.connector

# Read Barcode
def getBarcode(row):
    scanner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        con = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            port = 3306, #for Mamp users
            database='test_barcode'
        )
        scanner.connect((row[2], int(row[3])))

        while True:
            time.sleep(0.4)
            
            res = scanner.recv(100).decode()
            
            if (len(res.strip())):      
                try:
                    tmp = res.split()
                    for x in tmp:
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        db2 = con.cursor()
                        db2query = "INSERT into raw_packing_masters(machine_id,plant_id,line_id,barcode,created_at,updated_at) VALUES( %s,'%s','%s',%s,%s,%s )"
                        db2value = (row[0],row[4],row[5],res.strip(),timestamp,timestamp)
                        db2.execute(db2query,db2value)
                        con.commit()
                        print("Packing Entry : ",res)
                        print("Reader : ",row[2])
                    
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