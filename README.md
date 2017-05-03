# Python-Keylogger
###### by kchang33 and ywu100
A Keylogger for CS460 Final Project

(Tested on Windows 10, python version 2.7.13)
Note: Python 3 users may experience issues when attempting to build the executable file
## Setting up:
1. Get Packages needed to compile:
 - pynput 
 - pyinstaller (tested on version 3.2.1)

```
 pip install pynput
 pip install pyinstaller
```
2. Run **setup.bat**.
3. Navigate to the newly created **dist** folder. If the setup was successful then **keylogger.exe** should be there.

The current email target is the sender. Its login information is located in the python script. The destination can be changed via the destEmail variable.
