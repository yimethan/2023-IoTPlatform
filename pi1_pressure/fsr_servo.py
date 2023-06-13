# 압력-서보 최종
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

FSR = 4  # 압력센서 = BCM 4번(물리번호 7번)
SERVO1 = 18  # 서보모터1 = BCM 18번(물리번호 12번)
SERVO2 = 23  # 서보모터2 = BCM 23번(물리번호 16번)

# 압력센서
GPIO.setup(FSR, GPIO.IN)

# 서보 모터
GPIO.setwarnings(False)  # 이미 사용 중인 채널에 대한 경고 무시
GPIO.setup(SERVO1, GPIO.OUT)
GPIO.setup(SERVO2, GPIO.OUT)
servo1 = GPIO.PWM(SERVO1, 50)  # PWM 주파수 설정
servo2 = GPIO.PWM(SERVO2, 50)  # PWM 주파수 설정

# 서보 모터를 초기 위치로 설정
servo1.start(0)
servo2.start(0)
time.sleep(1)
servo1.ChangeDutyCycle(0)
servo2.ChangeDutyCycle(0)
time.sleep(1)

try:
    # 압력 패드가 눌려있는 동안에만 "Under Pressure"를 출력하고 서보 모터를 동작
    prev_input = 0  # 이전 입력 상태를 저장할 변수 초기화
    while True:
        # 압력센서 값 읽음
        input = GPIO.input(FSR)

        # 이전 입력이 낮았고 현재 입력이 높은 경우, 압력 패드가 눌려진 것으로 간주
        if not prev_input and input:
            # 누를 동안에만 "Under Pressure"를 출력하고 서보 모터 동작
            start_time = time.time()
            while time.time() - start_time < 0.7:  # 3초 동안 동작
                if input:
                    print("Under Pressure")
                    # 서보 모터를 움직이는 코드 추가
                    servo1.ChangeDutyCycle(6.5)  # 오른쪽
                    servo2.ChangeDutyCycle(7.5)  # 왼쪽
                    time.sleep(0.5)
                input = GPIO.input(FSR)
                time.sleep(0.1)
            # 서보모터 정지
            servo1.ChangeDutyCycle(0)  # 90도 위치
            servo2.ChangeDutyCycle(0)  # 90도 위치
            # 압력이 없는 상태를 3초 동안 감지
            start_time = time.time()
            while time.time() - start_time < 1:
                if not input:
                    time.sleep(3) # 압력이 없는 걸 감지하고 3초 후 원래 자리로 돌아가게
                    print("No Pressure")
                    # 서보 모터를 반대로
                    servo1.ChangeDutyCycle(7.5)  # 왼쪽
                    servo2.ChangeDutyCycle(6.5)  # 오른쪽
                    time.sleep(0.5)
                input = GPIO.input(FSR)
                time.sleep(0.1)
            # 서보모터 정지
            servo1.ChangeDutyCycle(0)  # 90도 위치
            servo2.ChangeDutyCycle(0)  # 90도 위치

            # 압력이 다시 감지되면 이전 동작을 반복
            prev_input = input
            continue

        # 이전 입력 값과 현재 입력 값이 같은 경우에는 이전 상태를 유지
        if prev_input == input:
            time.sleep(0.1)
            continue

        # 입력 값이 바뀐 경우, 이전 입력 값을 현재 입력 값으로 업데이트
        prev_input = input

    
except KeyboardInterrupt:
    # GPIO 정리
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()