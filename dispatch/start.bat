echo %DATE% - Started >> C:\barcode\dispatch\log.txt

FOR /F "tokens=2 delims= " %%P IN ('tasklist /FO Table /M /NH ^| Find /i "python3.9.exe"') DO (TASKKILL /PID %%P /F)
echo %DATE% - Killed >> C:\batfile\dispatch\log.txt

python C:\barcode\dispatch\dispatch.py
echo %DATE% - Started New Instance >> C:\barcode\dispatch\log.txt