echo %DATE% - Started >> C:\barcode\bat-log.txt

PowerShell C:\barcode\kill.ps1
echo %DATE% -  Killed >> C:\barcode\bat-log.txt

python ../../../barcode/init.py
echo %DATE% - Started New Instance >> C:\barcode\bat-log.txt