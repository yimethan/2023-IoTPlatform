import RPi.GPIO as GPIO 
GPIO.setwarnings(False) # 이미 사용 중인 채널에 대한 경고 무시
GPIO.setmode(GPIO.BOARD) 
from time import sleep, time

# 핀 번호
PIN_SERVO = 12
# or 33 (for PWM)

GPIO.setup(PIN_SERVO, GPIO.OUT)

pwm_frequency = 50

# 서보 모터를 초기 위치로 설정
pwm = GPIO.PWM(PIN_SERVO, pwm_frequency) # PWM 주파수 설정
pwm.start(0)

start_time = time()
while time() - start_time < .5:
    pwm.ChangeDutyCycle(6.5)
pwm.ChangeDutyCycle(0)
sleep(0.1)

print("Gas on")
pwm.stop()
GPIO.cleanup()