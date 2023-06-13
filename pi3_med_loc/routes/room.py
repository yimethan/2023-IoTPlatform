import RPi.GPIO as GPIO 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
from time import sleep
import json
import paho.mqtt.client as mqtt
import ssl
import sys

def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))
    
client = mqtt.Client()
client.on_connect = on_connect
client.tls_set(ca_certs='/home/User/term_project/routes/AmazonRootCA1.pem',
               certfile='/home/User/term_project/routes/certificate.pem.crt',
               keyfile='/home/User/term_project/routes/private.pem.key',
               tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect('x-ats.iot.ap-northeast-2.amazonaws.com', 8883, 60)
sleep(2)

PIN1 = 16
PIN2 = 18

GPIO.setup(PIN1, GPIO.IN)
GPIO.setup(PIN2, GPIO.IN)

last_room = -1
curr_room = 1
        
while True:
    if GPIO.input(PIN1) == GPIO.HIGH:
        if GPIO.input(PIN2) == GPIO.HIGH:
            print('pin 1 high, pin 2 high')
        if GPIO.input(PIN2) == GPIO.LOW:
            print('pin 1 high, pin 2 low')
            curr_room = 1
    if GPIO.input(PIN1) == GPIO.LOW:
        if GPIO.input(PIN2) == GPIO.HIGH:
            print('pin 1 low, pin 2 high')
            curr_room = 2
        if GPIO.input(PIN2) == GPIO.LOW:
            print('pin 1 low, pin 2 low')
            
    print('Current room:', curr_room)

    if curr_room != last_room:          
        if curr_room == 1: # 현재 거실
            client.publish('room', payload='1', qos=0, retain=False)
        elif curr_room == 2: # 현재 침실
            client.publish('room', payload='2', qos=0, retain=False)
            
        print('Location updated')
        sleep(3)