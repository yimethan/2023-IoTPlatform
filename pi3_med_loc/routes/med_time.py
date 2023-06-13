import RPi.GPIO as GPIO 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
from time import sleep
from datetime import datetime
import pyrebase
import paramiko
 
cli = paramiko.SSHClient()
cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

cli.connect('192.168.0.x', port=22, username='x', password='x') # ssh in my laptop

firebaseConfig = {
  'x':'x'
}

firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()

def check_time(h, m):
    # print(datetime.now().hour, datetime.now().minute)
    
    if int(h) == datetime.now().hour and int(m) == datetime.now().minute:
        print("Time to take your meds")
        stdin, stdout, stderr = cli.exec_command("afplay /Users/x/Downloads/rpi_sound.mp3")
        lines = stdout.readlines()
        print(''.join(lines))

try:

    while True:
        
        data = dict(database.child("HomeKeeper").get().val())
        # print(data)
        
        check_time(data['morning_hour'], data['morning_min'])
        check_time(data['noon_hour'], data['noon_min'])
        check_time(data['dinner_hour'], data['dinner_min'])
        
except KeyboardInterrupt:
    cli.close()
    GPIO.cleanup()
    exit()