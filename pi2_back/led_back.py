import RPi.GPIO as GPIO
import spidev
import time

GPIO.setwarnings(False)  # GPIO 경고 비활성화

spi = spidev.SpiDev()  # SPI 열기
spi.open(0, 0)
spi.max_speed_hz = 1000000  # SPI 속도 설정

SERVO = 12
TRIG = 16
ECHO = 18
PIN_LED = 22

def Spi_Read(channel):  # 채널의 값을 읽기
    adc = spi.xfer2([1, (8 + channel) << 4, 0])  # single ended 모드로 channel
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

def main():
    #조이-서보
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SERVO, GPIO.OUT)
    servo = GPIO.PWM(SERVO, 50)
    servo.start(0)
    # 초음파-LED
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.setup(PIN_LED, GPIO.OUT)

    try:
        while True:
            
            #조이-서보
            vry_pos = Spi_Read(2)  # y의 값을 읽음
            time.sleep(0.5)

            if vry_pos >= 1000:
                servo.ChangeDutyCycle(6.8)  # 오른쪽
                print(vry_pos)
            elif vry_pos <= 400:
                servo.ChangeDutyCycle(7.5)  # 왼쪽
                print(vry_pos)
            else:
                servo.ChangeDutyCycle(0)  # 중지
                print(vry_pos)

            #초음파-LED
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            print("Distance: {} cm".format(distance))

            if distance <= 20:
                GPIO.output(PIN_LED, GPIO.HIGH)
            else:
                GPIO.output(PIN_LED, GPIO.LOW)

            time.sleep(1)

    except KeyboardInterrupt:
        pass

    servo.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    main()