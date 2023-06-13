import RPi.GPIO as GPIO 
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD) 
from datetime import datetime
from picamera import PiCamera
from time import sleep, time
import os

print("save_pic.py start")

import pyrebase


GPIO.setmode(GPIO.BOARD)

TRIG_PIN = 16
ECHO_PIN = 18

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

firebaseConfig = {
  'x':'x'
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
camera = PiCamera()

count = 1

def measure_distance():
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    pulse_start = time()
    pulse_end = time()

    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time()

    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

try:
    while True:
        distance = measure_distance()
        print("Distance:", distance, "cm")

        if distance <= 5:
            start_time = time()
            elapsed_time = 0
            while elapsed_time < 3:
                elapsed_time = time() - start_time
                sleep(0.1)

            print("Person detected!")
            now = datetime.now()
            dt = now.strftime("%d%m%Y%H:%M:%S")
            name = str(count) + '.jpg'
            camera.capture(name)
            storage.child(name).put(name)
            os.remove(name)
            count += 1
            if count == 4:
                count = 1
            print("Image saved:", name)

        sleep(0.1)

except KeyboardInterrupt:
    camera.close()
    GPIO.cleanup()
    exit()
