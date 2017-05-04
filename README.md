# Python-Keylogger
###### by kchang33 and ywu100
A Keylogger for CS460 Final Project

Creates an windows executable file that runs in the background and tracks the keystrokes of the user. It then send the collected data to a specified email address in batches of relatively constant length along with the victim's IP address, hostname, username, and system configurations.

(Tested on Windows 10, python version 2.7.13, pyinstaller version 3.2.1)

NOTE: Python 3 users may experience issues when attempting to build the executable file
## Setting up:
#### 1. fill in the following in keylogger.py:
* Destination email Address (DEST\_EMAIL): The email to send results to. The current email target is the source email. 
* Source Email Information (SRC\_EMAIL/SRC\_PWD): This is the email that the result are sent from. 
* Buffer Size (DATA\_BUFFER\_SIZE): The number of characters that are collected before the email is sent.

#### 2. Run **setup.bat**.

This will install the required dependencies (_pyinstaller_ and _pynput_) and create an exe file. 

#### 3. Navigate to the newly created **dist** folder. If the setup was successful then **keylogger.exe** should be there.

#### 4. Run **keylogger.exe** on victim device.
