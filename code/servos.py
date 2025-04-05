from machine import Pin, PWM
from time import sleep

DOWN_A, UP_A = 130, 0
DOWN_B, UP_B = 30, 160

servo_A = PWM(Pin(8))
servo_A.freq(50)
servo_B = PWM(Pin(9))
servo_B.freq(50)

def set_angle_A(angle):
    min_duty = 1500  # Needs to be tested
    max_duty = 8000  # Needs to be tested
    duty = int((angle / 180) * (max_duty - min_duty) + min_duty)
    servo_A.duty_u16(duty)

def set_angle_B(angle):
    min_duty = 1500  # Needs to be tested
    max_duty = 8000  # Needs to be tested
    duty = int((angle / 180) * (max_duty - min_duty) + min_duty)
    servo_B.duty_u16(duty)
    
def lift():
    set_angle_A(UP_A)
    sleep(0.03) # B executes faster
    set_angle_B(UP_B)
    sleep(1)
    set_angle_A(DOWN_A)
    sleep(0.03)
    set_angle_B(DOWN_B)
    
lift()
