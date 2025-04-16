from machine import Pin, PWM
from time import sleep

DOWN_A, UP_A = 130, 0
DOWN_B, UP_B = 30, 160

servo_A = PWM(Pin(8))
servo_A.freq(50)
servo_B = PWM(Pin(9))
servo_B.freq(50)

def init_servos():
    servo_A = PWM(Pin(8))
    servo_A.freq(50)
    servo_B = PWM(Pin(9))
    servo_B.freq(50)

def set_angle_A(angle):
    min_duty = 1500
    max_duty = 8000
    duty = int((angle / 180) * (max_duty - min_duty) + min_duty)
    servo_A.duty_u16(duty)

def set_angle_B(angle):
    min_duty = 1500
    max_duty = 8000
    duty = int((angle / 180) * (max_duty - min_duty) + min_duty)
    servo_B.duty_u16(duty)

def lift():
    init_servos()
    set_angle_B(UP_B)
    set_angle_A(UP_A)
    sleep(1)
    set_angle_B(DOWN_B)
    set_angle_A(DOWN_A)
    sleep(0.5)
    servo_A.deinit()
    servo_B.deinit()

if __name__ == "__main__":
    lift()
