from _thread import *
import threading
from reader import Reader
import logging
import time
import subprocess
from tendo import singleton

logging.basicConfig(filename="reader.log")
logging.warning('Reader Started')

try:
    me = singleton.SingleInstance()
except:
    logging.warning('Killing Existing Proces')
    cmd = r"""taskkill.exe /F /PID $(Get-WmiObject Win32_Process -Filter "name = 'python.exe'" | Where-Object {$_.CommandLine -like '*barcode.py'} | Select -ExpandProperty ProcessId)  """
    subprocess.call("./kill.bash", shell=true) 

con = Reader.connect()

mycursor = con.cursor()
mycursor.execute("SELECT * FROM barcode_machine_masters")
myresult = mycursor.fetchall()
# End : DB Connection

# Init Thread
if __name__ == "__main__":

    while True:
        for key,i in enumerate(myresult):
            temp = 'T' + str(key)
            temp = threading.Thread(target=Reader(i))
            temp.daemon = True
            print(temp)
            temp.start()

        for instance in Reader.instances:
            print(instance.name)
        
        time.sleep(60)
        




